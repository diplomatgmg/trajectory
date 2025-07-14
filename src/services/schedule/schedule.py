from datetime import datetime
import logging

from schemas.schedule import Schedule, TimeSlot
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

    def get_busy_time_slots(self, date_str: str) -> list[TimeSlot]:
        """Возвращает список занятых промежутков для указанной даты."""
        logger.debug("Getting busy periods for %s", date_str)

        target_date = _parse_iso_date_string(date_str).date()
        target_workday = next((day for day in self.schedule.days if day.date == target_date), None)
        if not target_workday:
            raise WorkdayNotFoundError(f"Workday {target_date} not found in schedule")

        busy_slots: list[TimeSlot] = [slot for slot in self.schedule.timeslots if slot.day_id == target_workday.id]
        logger.debug("Found %s busy slots for date %s", len(busy_slots), target_date)

        return busy_slots
