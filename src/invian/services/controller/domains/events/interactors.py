from datetime import datetime

from invian.services.controller.data.repositories.events import EventsRepository
from invian.services.controller.domains.events.entities import EventEntity

__all__ = ("EventsInteractor",)


class EventsInteractor:
    def __init__(self, repository: EventsRepository) -> None:
        self.__repository = repository

    async def get_for_period(self, period: datetime) -> list[int]:
        return await self.__repository.get_for_period(period)

    async def create(self, event: EventEntity) -> None:
        await self.__repository.create(event)
