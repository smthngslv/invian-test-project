from invian.services.sensor.data.repositories.measurements import MeasurementsRepository

__all__ = ("MeasurementsInteractor",)


class MeasurementsInteractor:
    def __init__(self, repository: MeasurementsRepository) -> None:
        self.__repository = repository

    async def send(self, payload: int) -> None:
        await self.__repository.send(payload)

    async def shutdown(self) -> None:
        await self.__repository.shutdown()
