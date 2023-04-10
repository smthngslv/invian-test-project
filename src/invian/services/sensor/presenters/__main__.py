import asyncio
import random
from asyncio import Task

from tqdm import tqdm

from invian.common import settings
from invian.services.sensor.presenters.sensor import Sensor


async def main(concurrency: int) -> None:
    progress = tqdm()

    async with Sensor(settings.CONTROLLER_API_URL) as sensor:
        tasks: dict[int, Task] = {}
        count = 0

        while True:
            for index in list(tasks.keys()):
                if tasks[index].done():
                    await tasks.pop(index)
                    progress.update()
                    progress.set_description("\n")

            if len(tasks) < concurrency:
                task = sensor.send(random.randint(0, 100))  # noqa: S311
                tasks[count] = asyncio.create_task(task)
                count += 1
                continue

            await asyncio.sleep(0.1)


if __name__ == "__main__":
    asyncio.run(main(32))
