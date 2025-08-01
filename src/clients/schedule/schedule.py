from httpx import URL

from clients.base import BaseClient
from schemas.schedule import Schedule


__all__ = ["ScheduleClient"]


class ScheduleClient(BaseClient):
    url = URL("https://ofc-test-01.tspb.su/test-task/")

    async def get_schedules(self) -> Schedule:
        response = await self.client.get(self.url)
        response.raise_for_status()

        return Schedule.model_validate(response.json())
