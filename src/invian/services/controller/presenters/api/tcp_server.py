import asyncio
from asyncio import Lock, Queue, QueueFull, Server, StreamReader, StreamWriter, TimeoutError
from contextlib import suppress
from dataclasses import asdict
from datetime import datetime
from logging import getLogger
from typing import Any
from urllib.parse import urlsplit

import msgpack

from invian.services.controller.domains.controls.entities import ControlEntity

__all__ = ("TCPServer",)


class TCPServer:
    def __init__(self, url: str) -> None:
        try:
            _, netloc, _, _, _ = urlsplit(url, scheme="tcp")
            self.__host, self.__port = netloc.split(":")

        except Exception as exception:
            message = "URL should be in the following form: tcp://host:port."
            raise ValueError(message) from exception

        self.__lock = Lock()
        self.__server: Server | None = None
        self.__queues: dict[tuple[str, int], Queue] = {}

    @property
    def is_started(self) -> bool:
        return self.__server is not None and self.__server.is_serving()

    def publish(self, control: ControlEntity) -> None:
        data = msgpack.packb(asdict(control), default=self.__pack)

        for queue in self.__queues.values():
            with suppress(QueueFull):
                queue.put_nowait(data)

    async def start(self, *, block: bool = True) -> None:
        async with self.__lock:
            if self.__server is not None:
                return

            self.__server = await asyncio.start_server(self.__handler, self.__host, self.__port)
            await (self.__server.serve_forever() if block else self.__server.start_serving())

    async def stop(self) -> None:
        async with self.__lock:
            if self.__server is None:
                return

            self.__server.close()
            await self.__server.wait_closed()
            self.__server = None

    async def __aenter__(self) -> None:
        await self.start()

    async def __aexit__(self, _, __, ___) -> None:
        await self.stop()

    async def __handler(self, _: StreamReader, writer: StreamWriter) -> None:
        queue: Queue = Queue(maxsize=1)
        address = writer.get_extra_info("peername")

        # Substitute to events.
        self.__queues[address] = queue

        try:
            while self.is_started and not writer.is_closing():
                try:
                    data = await asyncio.wait_for(queue.get(), timeout=0.1)

                except TimeoutError:
                    continue

                # Data + end of package.
                writer.write(data + b"\00\00\00\00")
                await writer.drain()

        except Exception as exception:
            getLogger().exception(f"Cannot send control: {exception}")

        finally:
            self.__queues.pop(address)

    @staticmethod
    def __pack(obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()

        message = f"Cannot encode: {obj}."
        raise TypeError(message)
