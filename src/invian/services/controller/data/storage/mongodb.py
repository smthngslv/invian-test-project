from motor.motor_asyncio import AsyncIOMotorClient

__all__ = ("MongoDBStorage",)


class MongoDBStorage:
    def __init__(self, url: str) -> None:
        self.__url = url
        self.__client: AsyncIOMotorClient | None = None

    @property
    def client(self) -> AsyncIOMotorClient:
        if self.__client is None:
            self.__client = AsyncIOMotorClient(self.__url)

        return self.__client

    async def shutdown(self) -> None:
        if self.__client is not None:
            self.__client.close()
