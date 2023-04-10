from datetime import datetime, timezone
from typing import Any

import orjson
from aiohttp import ClientSession

__all__ = ("MeasurementsRepository",)


class MeasurementsRepository:
    def __init__(self, url: str) -> None:
        self.__url = url.removesuffix("/")
        self.__session = ClientSession()

    async def send(self, payload: int) -> None:
        data = orjson.dumps(
            {"datetime": datetime.now(tz=timezone.utc).isoformat(), "payload": payload}, default=self.__pack
        )

        async with self.__session.post(
            f"{self.__url}/v1/events", data=data, headers={"Content-Type": "application/json"}
        ) as response:
            if response.status != 201:  # noqa: PLR2004
                message = f"Cannot send event (HTTP {response.status}): {await response.text()}"
                raise ValueError(message)

    async def shutdown(self) -> None:
        await self.__session.close()

    @staticmethod
    async def __pack(obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()

        message = f"Cannot encode: {obj}."
        raise TypeError(message)
