import asyncio
from asyncio import Event
from datetime import datetime, timedelta, timezone
from logging import getLogger

from invian.common.utils import round_to_interval
from invian.services.controller.data.repositories.controls import ControlsRepository
from invian.services.controller.data.repositories.events import EventsRepository
from invian.services.controller.data.storage.mongodb import MongoDBStorage
from invian.services.controller.data.storage.redis import RedisStorage
from invian.services.controller.domains.controls.interactors import ControlsInteractor
from invian.services.controller.domains.events.interactors import EventsInteractor
from invian.services.controller.presenters.api.tcp_server import TCPServer

__all__ = ("Worker",)


class Worker:
    def __init__(
        self,
        tcp_url: str,
        interval: int,
        *,
        redis_url: str | None = None,
        mongodb_url: str | None = None,
        redis_storage: RedisStorage | None = None,
        mongodb_storage: MongoDBStorage | None = None,
    ) -> None:
        self.__tcp_server = TCPServer(tcp_url)
        self.__interval = interval

        if redis_storage is None:
            if redis_url is None:
                message = "You should specify redis_url or redis_storage."
                raise ValueError(message)

            redis_storage = RedisStorage(redis_url)

        if mongodb_storage is None:
            if mongodb_url is None:
                message = "You should specify mongodb_url or mongodb_storage."
                raise ValueError(message)

            mongodb_storage = MongoDBStorage(mongodb_url)

        self.__redis_storage = redis_storage
        self.__mongodb_storage = mongodb_storage

        # Need to refresh every second.
        self.__lock = self.__redis_storage.connection.lock("invian-api-tcp-worker-lock", timeout=self.__interval)

        # Will be used to store and create aggregations.
        self.__interactor = ControlsInteractor(
            ControlsRepository(mongodb_storage), EventsInteractor(EventsRepository(redis_storage, interval)), interval
        )

        self.__is_stopped = Event()

    async def start(self) -> None:
        self.__is_stopped.clear()

        while not self.__is_stopped.is_set():
            try:
                await self.__worker()

            except Exception as exception:
                getLogger().exception(f"Worker has failed: {exception}")

            finally:
                await self.__tcp_server.stop()

    async def shutdown(self) -> None:
        self.__is_stopped.set()
        await self.__redis_storage.shutdown()
        await self.__mongodb_storage.shutdown()

    async def __worker(self) -> None:
        if not await self.__lock.acquire(blocking=True, blocking_timeout=0.1):
            return

        next_aggregation = round_to_interval(datetime.now(tz=timezone.utc), self.__interval)

        while not self.__is_stopped.is_set():
            if not self.__tcp_server.is_started:
                await self.__tcp_server.start(block=False)

            now = datetime.now(tz=timezone.utc)

            # Start aggregation.
            if now >= next_aggregation:
                # Create a control entity for previous period.
                control = await self.__interactor.create(next_aggregation - timedelta(seconds=self.__interval / 2))

                # Log.
                print(f"New control message: {control}", flush=True)  # noqa: T201

                # Publish to TCP.
                self.__tcp_server.publish(control)

                # Next aggregation in 5 seconds.
                next_aggregation += timedelta(seconds=self.__interval)

            # Heartbeat.
            await self.__lock.extend(additional_time=self.__interval, replace_ttl=True)

            # Sleap maximum 0.1 seconds.
            time_to_next_aggregation = (next_aggregation - now).total_seconds()
            await asyncio.sleep(min(0.1, max(0.0, time_to_next_aggregation)))
