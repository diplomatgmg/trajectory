from collections.abc import AsyncGenerator
from datetime import date, time
from typing import Any
from unittest.mock import patch

import pytest
import pytest_asyncio

from schemas.schedule import Schedule
from services.schedule import ScheduleService
from services.schedule.exceptions import InvalidTimeFormatError, WorkdayNotFoundError


@pytest_asyncio.fixture
async def schedule_service(sample_schedule_data: dict[str, Any]) -> AsyncGenerator[ScheduleService]:
    """Фикстура, которая мокирует API-клиент и создает экземпляр ScheduleService."""
    with patch("clients.schedule.ScheduleClient.get_schedules") as mock_get_data:
        mock_get_data.return_value = Schedule.model_validate(sample_schedule_data)

        schedule_data = await mock_get_data()
        service = ScheduleService(schedule_data)
        yield service


# ==========================
# get_busy_time_slots
# ==========================


def test_get_busy_timeslots_happy_path(schedule_service: ScheduleService) -> None:
    """Получение занятых слотов для даты, где они есть."""
    # 2025-02-15, 09:00 -> 21:00
    # slots: 09:00 -> 12:00, 17:30 -> 20:00
    busy_slots = schedule_service.get_busy_time_slots("2025-02-15")

    assert len(busy_slots) == 2

    assert busy_slots[0].start == time(9, 0)
    assert busy_slots[0].end == time(12, 0)

    assert busy_slots[1].start == time(17, 30)
    assert busy_slots[1].end == time(20, 0)


def test_get_busy_timeslots_no_slots(schedule_service: ScheduleService) -> None:
    """Получение занятых слотов для даты, где их нет"""
    busy_slots = schedule_service.get_busy_time_slots("2025-02-19")
    assert busy_slots == []


def test_get_busy_slots_non_existent_date(schedule_service: ScheduleService) -> None:
    """Попытка получить слоты для несуществующего рабочего дня."""
    with pytest.raises(WorkdayNotFoundError, match="Workday 2025-12-31 not found"):
        schedule_service.get_busy_time_slots("2025-12-31")


@pytest.mark.parametrize("invalid_date", ["2025/02/15", "15/02/2025", "not-a-date"])
def test_get_busy_slots_invalid_date_format(schedule_service: ScheduleService, invalid_date: str) -> None:
    """Тест: попытка получить слоты с неверным форматом даты."""
    with pytest.raises(InvalidTimeFormatError):
        schedule_service.get_busy_time_slots(invalid_date)


@pytest.mark.parametrize("invalid_time", ["25:70", "15-02-2025", "not-a-time"])
def test_is_timeslot_available_time_format(schedule_service: ScheduleService, invalid_time: str) -> None:
    """Тест: попытка получить слоты с неверным форматом даты."""
    with pytest.raises(InvalidTimeFormatError):
        schedule_service.is_timeslot_available("15-02-2025", invalid_time, "10:00")


# ==========================
# Тесты для get_free_timeslots
# ==========================


def test_get_free_timeslots_happy_path(schedule_service: ScheduleService) -> None:
    """Получение свободных слотов для обычного дня."""
    # 2025-02-15, 09:00 -> 21:00
    # slots: 09:00 -> 12:00, 17:30 -> 20:00
    free_slots = schedule_service.get_free_timeslots("2025-02-15")

    assert len(free_slots) == 2

    assert free_slots[0].start == time(12, 0)
    assert free_slots[0].end == time(17, 30)

    assert free_slots[1].start == time(20, 0)
    assert free_slots[1].end == time(21, 0)


def test_get_free_timeslots_day_with_no_busy_slots(schedule_service: ScheduleService) -> None:
    """Получение свободных слотов для дня, где все время свободно."""
    free_slots = schedule_service.get_free_timeslots("2025-02-19")

    assert len(free_slots) == 1

    assert free_slots[0].start == time(9, 0)
    assert free_slots[0].end == time(18, 0)


def test_get_free_timeslots_back_to_back_slots(schedule_service: ScheduleService) -> None:
    """Тест: свободные слоты для дня, где есть слоты идущие встык."""
    # 2025-02-18, 10:00 -> 18:00
    # slots: 10:00 -> 11:00, 11:30 -> 14:00, 14:00 -> 16:00, 17:00 -> 18:00

    free_slots = schedule_service.get_free_timeslots("2025-02-18")

    assert len(free_slots) == 2

    assert free_slots[0].start == time(11, 0)
    assert free_slots[0].end == time(11, 30)

    assert free_slots[1].start == time(16, 0)
    assert free_slots[1].end == time(17, 0)


# ==========================
# Тесты для is_timeslot_available
# ==========================


@pytest.mark.parametrize(
    ("start_time", "end_time", "expected"),
    [
        ("11:00", "14:30", True),  # Полностью свободный слот
        ("12:00", "13:00", True),  # Слот впритык с началом занятого
        ("08:00", "09:30", True),  # Слот впритык с концом занятого
        ("09:00", "10:00", False),  # Точное совпадение с занятым слотом
        ("09:15", "09:45", False),  # Запрашиваемый слот полностью внутри занятого
        ("10:30", "11:30", False),  # Пересечение в конце
        ("07:00", "08:00", False),  # Полностью до начала рабочего дня
        ("22:30", "23:00", False),  # Полностью после конца рабочего дня
        ("07:30", "08:30", False),  # Частично до начала рабочего дня
        ("21:30", "22:30", False),  # Частично после конца рабочего дня
    ],
)
def test_is_timeslot_available_various_scenarios(
    schedule_service: ScheduleService, start_time: str, end_time: str, expected: bool
) -> None:
    """Проверка доступности слота в различных ситуациях."""
    # 2025-02-16, 08:00 -> 22:00
    # slots: 09:30 -> 11:00, 14:30 -> 18:00,

    is_available = schedule_service.is_timeslot_available("2025-02-16", start_time, end_time)
    assert is_available is expected


@pytest.mark.parametrize(("start_time", "end_time"), [("11:00", "10:00"), ("12:00", "12:00")])
def test_is_timeslot_available_start_after_end(
    schedule_service: ScheduleService, start_time: str, end_time: str
) -> None:
    """Тест: проверка ошибки, если время начала >= времени окончания."""
    with pytest.raises(InvalidTimeFormatError, match="Start time must be before end time"):
        schedule_service.is_timeslot_available("2025-02-16", start_time, end_time)


# ==============================================================================
# Тесты для find_first_available_slot
# ==============================================================================


def test_find_first_available_slot_happy_path(schedule_service: ScheduleService) -> None:
    """Тест: поиск первого доступного слота достаточной продолжительности."""
    slots = schedule_service.find_first_available_slot(duration_minutes=60)

    assert len(slots) > 0

    assert slots[0].date == date(2025, 2, 15)
    assert slots[0].start == time(12, 0)
    assert slots[0].end == time(17, 30)


def test_find_first_available_slot_skips_to_next_day(schedule_service: ScheduleService) -> None:
    """Тест: поиск слота, когда на первом дне нет подходящих, но есть на втором."""
    # Ищем слот на 360 минут (6 часов).
    # На 2025-02-15 самый большой слот 12:00-17:30 (330 минут) - не подходит.
    # На 2025-02-16 есть 08:00-09:30 (90 мин), 11:00-14:30 (210 мин), 18:00-22:00 (240 мин) - тоже нет.
    # На 2025-02-17 есть 09:00-12:30 (210 мин) - тоже нет.
    # На 2025-02-19 весь день 09:00-18:00 (540 мин) свободен - подходит.
    slots = schedule_service.find_first_available_slot(duration_minutes=360)

    assert len(slots) == 1

    assert slots[0].date == date(2025, 2, 19)
    assert slots[0].start == time(9, 0)
    assert slots[0].end == time(18, 0)


def test_find_first_available_slot_no_slot_found(schedule_service: ScheduleService) -> None:
    """Тест: поиск слота, когда нет ни одного подходящего по длительности."""
    slots = schedule_service.find_first_available_slot(duration_minutes=9999)
    assert slots == []


def test_find_first_available_slot_zero_duration(schedule_service: ScheduleService) -> None:
    """Тест: поиск слота с нулевой продолжительностью."""
    slots = schedule_service.find_first_available_slot(duration_minutes=0)

    assert len(slots) > 0

    assert slots[0].date == date(2025, 2, 15)
    assert slots[0].start == time(12, 0)
