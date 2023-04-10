from datetime import timedelta

from fastapi import status

from invian.common import settings
from invian.services.controller.data.repositories.controls import ControlsRepository
from invian.services.controller.data.repositories.events import EventsRepository
from invian.services.controller.data.storage.mongodb import MongoDBStorage
from invian.services.controller.data.storage.redis import RedisStorage
from invian.services.controller.domains.controls.interactors import ControlsInteractor
from invian.services.controller.domains.events.interactors import EventsInteractor
from invian.services.controller.presenters.api.endpoints.events import router

__all__ = ("create",)

from invian.services.controller.presenters.api.endpoints.history.schemas import HistoryEntry

# Initialize interactor.
interactor = ControlsInteractor(
    ControlsRepository(MongoDBStorage(settings.MONGODB_URL)),
    EventsInteractor(EventsRepository(RedisStorage(settings.REDIS_URL), settings.INTERVAL)),
    settings.INTERVAL,
)


@router.get("", status_code=status.HTTP_201_CREATED, response_model=list[HistoryEntry])
async def create() -> list[HistoryEntry]:
    history: list[HistoryEntry] = []

    for control in await interactor.get():
        if len(history) == 0 or history[-1].status != control.status:
            history.append(
                HistoryEntry(
                    start=control.datetime,
                    end=control.datetime + timedelta(seconds=settings.INTERVAL),
                    status=control.status,
                )
            )
            continue

        history[-1].end = control.datetime + timedelta(seconds=settings.INTERVAL)

    return history
