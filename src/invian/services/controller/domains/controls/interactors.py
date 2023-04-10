from datetime import datetime

from invian.common.utils import round_to_interval
from invian.services.controller.data.repositories.controls import ControlsRepository
from invian.services.controller.domains.controls.entities import ControlEntity
from invian.services.controller.domains.controls.enums import ControlStatus
from invian.services.controller.domains.events.interactors import EventsInteractor

__all__ = ("ControlsInteractor",)


class ControlsInteractor:
    def __init__(self, repository: ControlsRepository, interactor: EventsInteractor, interval: int) -> None:
        self.__repository = repository
        self.__interactor = interactor
        self.__interval = interval

    async def get(self) -> list[ControlEntity]:
        return await self.__repository.get()

    async def create(self, period: datetime) -> ControlEntity:
        period = round_to_interval(period, self.__interval)

        # Get payloads for given period.
        payloads = await self.__interactor.get_for_period(period)

        # Simple rule for status.
        status = len(payloads) != 0 and sum(payloads) / len(payloads) >= 50  # noqa: PLR2004

        # Create control entity.
        control = ControlEntity(
            datetime=period, status=ControlStatus.UP if status else ControlStatus.DOWN
        )  # type: ignore[call-arg]
        await self.__repository.create(control)

        return control
