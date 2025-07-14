from collections.abc import AsyncGenerator
from typing import Any

import httpx
import pytest
import pytest_asyncio
import respx

from clients.schedule import ScheduleClient
from schemas.schedule import Schedule


@pytest.fixture
def sample_schedule_data() -> dict[str, Any]:
    """Фикстура с примером валидного ответа от API."""
    return {
        "days": [{"id": 1, "date": "2025-02-15", "start": "09:00", "end": "21:00"}],
        "timeslots": [{"id": 1, "day_id": 1, "start": "17:30", "end": "20:00"}],
    }


@pytest_asyncio.fixture
async def schedule_client() -> AsyncGenerator[ScheduleClient]:
    """Фикстура, создающая экземпляр клиента."""
    async with httpx.AsyncClient() as client:
        yield ScheduleClient(client)


@pytest.mark.asyncio
async def test_get_schedules_success(
    schedule_client: ScheduleClient,
    sample_schedule_data: dict[str, Any],
) -> None:
    """Тест успешного получения и валидации расписания."""
    with respx.mock:
        respx.get(schedule_client.url).mock(return_value=httpx.Response(200, json=sample_schedule_data))

        schedules = await schedule_client.get_schedules()

        assert isinstance(schedules, Schedule)
        assert len(schedules.days) == 1
        assert schedules.days[0].id == 1


@pytest.mark.asyncio
async def test_get_schedules_http_error(schedule_client: ScheduleClient) -> None:
    """Тест обработки ошибки HTTP."""
    with respx.mock:
        respx.get(schedule_client.url).mock(return_value=httpx.Response(404, json={"detail": "Not Found"}))

        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            await schedule_client.get_schedules()

        assert exc_info.value.response.status_code == 404
