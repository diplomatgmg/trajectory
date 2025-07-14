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

    schedule_service = ScheduleService(schedules)

    schedule_service.find_first_available_slot(60)


if __name__ == "__main__":
    uvloop.run(main())
