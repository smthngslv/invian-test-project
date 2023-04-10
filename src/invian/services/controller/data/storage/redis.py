import aioredis
from aioredis import Redis

__all__ = ("RedisStorage",)


class RedisStorage:
    def __init__(self, url: str) -> None:
        self.__connection = aioredis.from_url(url)

    @property
    def connection(self) -> Redis:
        return self.__connection

    async def shutdown(self) -> None:
        await self.__connection.close()
