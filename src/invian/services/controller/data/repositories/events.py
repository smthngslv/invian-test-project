from datetime import datetime

from invian.common.utils import round_to_interval
from invian.services.controller.data.storage.redis import RedisStorage
from invian.services.controller.domains.events.entities import EventEntity

__all__ = ("EventsRepository",)


class EventsRepository:
    def __init__(self, storage: RedisStorage, interval: int) -> None:
        self.__storage = storage
        self.__interval = interval

    async def get_for_period(self, period: datetime) -> list[int]:
        return [int(payload) for payload in await self.__storage.connection.lrange(self.__get_key(period), 0, -1)]

    async def create(self, event: EventEntity) -> None:
        key = self.__get_key(event.datetime)
        await self.__storage.connection.rpush(key, event.payload)
        await self.__storage.connection.expire(key, self.__interval)

    def __get_key(self, period: datetime) -> str:
        return f"events-{int(round_to_interval(period, self.__interval).timestamp())}"
