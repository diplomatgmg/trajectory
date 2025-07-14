from datetime import date, datetime
import logging

from schemas.schedule import Day, FreeTimeSlot, Schedule, TimeSlot
from services.schedule.exceptions import ScheduleServiceError, WorkdayNotFoundError


__all__ = ["ScheduleService"]

logger = logging.getLogger(__name__)


def _parse_iso_date_string(date: str) -> datetime:
    try:
        return datetime.fromisoformat(date)
    except ValueError as e:
        raise ScheduleServiceError(
            f"Invalid date format: '{date}'. Expected ISO format 'YYYY-MM-DD' or 'YYYY-MM-DDTHH:MM:SS'."
        ) from e


class ScheduleService:
    def __init__(self, schedule: Schedule) -> None:
        self.schedule = schedule

    def _get_target_workday(self, target_date: date) -> Day:
        """Возвращает рабочий день для указанной даты."""
        logger.debug("Getting workday for %s", target_date)

        target_workday = next((day for day in self.schedule.days if day.date == target_date), None)
        if not target_workday:
            raise WorkdayNotFoundError(f"Workday {target_date} not found in schedule")

        logger.debug("Found workday %s for date %s", target_workday.id, target_date)
        return target_workday

    def get_busy_time_slots(self, date_str: str) -> list[TimeSlot]:
        """Возвращает список занятых промежутков для указанной даты."""
        logger.debug("Getting busy periods for %s", date_str)

        target_date = _parse_iso_date_string(date_str).date()
        target_workday = self._get_target_workday(target_date)

        busy_slots: list[TimeSlot] = [slot for slot in self.schedule.timeslots if slot.day_id == target_workday.id]
        busy_slots.sort(key=lambda ts: ts.start)

        logger.debug("Found %s busy slots for date %s: %s", len(busy_slots), target_date, busy_slots)

        return busy_slots

    def get_free_timeslots(self, date_str: str) -> list[FreeTimeSlot]:
        """Возвращает список свободных промежутков для указанной даты."""

        target_date = _parse_iso_date_string(date_str).date()
        target_workday = self._get_target_workday(target_date)
        busy_slots = self.get_busy_time_slots(date_str)

        free_periods: list[FreeTimeSlot] = []
        last_busy_end_time = target_workday.start

        # Итерируемся по занятым слотам, чтобы найти свободное окно
        for slot in busy_slots:
            if last_busy_end_time < slot.start:
                free_periods.append(FreeTimeSlot(start=last_busy_end_time, end=slot.start))

            last_busy_end_time = max(last_busy_end_time, slot.end)

        # Проверяем свободное окно после последнего занятого слота
        if last_busy_end_time < target_workday.end:
            free_periods.append(FreeTimeSlot(start=last_busy_end_time, end=target_workday.end))

        return free_periods
