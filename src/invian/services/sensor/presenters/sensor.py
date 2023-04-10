from invian.services.sensor.data.repositories.measurements import MeasurementsRepository
from invian.services.sensor.domains.measurements.interactors import MeasurementsInteractor

__all__ = ("Sensor",)


class Sensor:
    def __init__(self, url: str) -> None:
        self.__interactor = MeasurementsInteractor(MeasurementsRepository(url))

    async def send(self, payload: int) -> None:
        await self.__interactor.send(payload)

    async def shutdown(self) -> None:
        await self.__interactor.shutdown()

    async def __aenter__(self) -> "Sensor":
        return self

    async def __aexit__(self, _, __, ___) -> None:
        await self.shutdown()
