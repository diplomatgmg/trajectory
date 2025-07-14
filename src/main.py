import logging

from httpx import AsyncClient
import uvloop

from clients.schedule import ScheduleClient
from logger.factory import setup_logger
from services.schedule import ScheduleService


setup_logger()

logger = logging.getLogger(__name__)


async def main() -> None:
    async with AsyncClient() as client:
        schedule_client = ScheduleClient(client)
        schedules = await schedule_client.get_schedules()
    logger.info(schedules)

    schedule_service = ScheduleService(schedules)

    date = "2025-02-15"
    p = schedule_service.get_free_timeslots(date)
    logger.error(p)


if __name__ == "__main__":
    uvloop.run(main())
