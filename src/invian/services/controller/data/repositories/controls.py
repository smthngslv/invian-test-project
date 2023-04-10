from dataclasses import asdict

from invian.services.controller.data.storage.mongodb import MongoDBStorage
from invian.services.controller.domains.controls.entities import ControlEntity

__all__ = ("ControlsRepository",)


class ControlsRepository:
    def __init__(self, storage: MongoDBStorage) -> None:
        self.__storage = storage

    async def get(self) -> list[ControlEntity]:
        return [ControlEntity(**control) async for control in self.__storage.client.invian.controls.find({})]

    async def create(self, control: ControlEntity) -> None:
        await self.__storage.client.invian.controls.insert_one(asdict(control))
