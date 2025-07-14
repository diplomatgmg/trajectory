from collections.abc import AsyncGenerator
from datetime import time
from typing import Any
from unittest.mock import patch

import pytest_asyncio

from schemas.schedule import Schedule
from services.schedule import ScheduleService


@pytest_asyncio.fixture
async def schedule_service(sample_schedule_data: dict[str, Any]) -> AsyncGenerator[ScheduleService]:
    """Фикстура, которая мокирует API-клиент и создает экземпляр ScheduleService."""
    with patch("clients.schedule.ScheduleClient.get_schedules") as mock_get_data:
        mock_get_data.return_value = Schedule.model_validate(sample_schedule_data)

        schedule_data = await mock_get_data()
        service = ScheduleService(schedule_data)
        yield service


def test_get_busy_timeslots_happy_path(schedule_service: ScheduleService) -> None:
    """Получение занятых слотов для даты, где они есть."""
    busy_slots = schedule_service.get_busy_time_slots("2025-02-15")

    assert len(busy_slots) == 2
    assert busy_slots[0].start == time(9, 0)
    assert busy_slots[1].end == time(20, 0)
