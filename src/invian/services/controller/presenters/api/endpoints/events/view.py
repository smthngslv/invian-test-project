from fastapi import status

from invian.common import settings
from invian.services.controller.data.repositories.events import EventsRepository
from invian.services.controller.data.storage.redis import RedisStorage
from invian.services.controller.domains.events.entities import EventEntity
from invian.services.controller.domains.events.interactors import EventsInteractor
from invian.services.controller.presenters.api.endpoints.events import router

__all__ = ("create",)

# Initialize interactor.
interactor = EventsInteractor(EventsRepository(RedisStorage(settings.REDIS_URL), settings.INTERVAL))


@router.post("", status_code=status.HTTP_201_CREATED, response_model=EventEntity)
async def create(event: EventEntity) -> EventEntity:
    await interactor.create(event)
    return event
