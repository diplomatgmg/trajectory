import logging

from httpx import AsyncClient
import uvloop

from clients.schedule import ScheduleClient


logger = logging.getLogger(__name__)


async def main() -> None:
    async with AsyncClient() as client:
        schedule_client = ScheduleClient(client)
        await schedule_client.get_schedule()


if __name__ == "__main__":
    uvloop.run(main())
