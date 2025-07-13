import logging

from httpx import AsyncClient
import uvloop

from clients.schedule import ScheduleClient


logger = logging.getLogger(__name__)


async def main() -> None:
    async with AsyncClient() as client:
        schedule_client = ScheduleClient(client)
        schedules = await schedule_client.get_schedules()
    print('11291456')
    logger.info(schedules, 5)


if __name__ == "__main__":
    uvloop.run(main())
