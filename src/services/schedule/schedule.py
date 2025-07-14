from datetime import UTC, date, datetime, time, timedelta
import logging

from schemas.schedule import AvailableTimeSlot, Day, FreeTimeSlot, Schedule, TimeSlot
from services.schedule.exceptions import InvalidTimeFormatError, WorkdayNotFoundError


__all__ = ["ScheduleService"]

logger = logging.getLogger(__name__)


def _parse_iso_date_string(date_str: str) -> datetime:
    try:
        return datetime.fromisoformat(date_str)
    except ValueError as e:
        raise InvalidTimeFormatError(
            f"Invalid date format: '{date_str}'. Expected ISO format 'YYYY-MM-DD' or 'YYYY-MM-DDTHH:MM:SS'."
        ) from e


def _parse_time_string(time_str: str) -> time:
    try:
        return datetime.strptime(time_str, "%H:%M").time()  # noqa: DTZ007 tz роли не играет
    except ValueError as e:
        raise InvalidTimeFormatError(f"Invalid time format: '{time_str}'. Expected format 'HH:MM' ro.") from e


class ScheduleService:
    def __init__(self, schedule: Schedule) -> None:
        self.schedule = schedule
        self._target_workday_cache: dict[date, Day] = {}

    def _get_target_workday(self, target_date: date) -> Day:
        """Возвращает рабочий день для указанной даты."""
        logger.debug("Getting workday for %s", target_date)

        if target_workday := self._target_workday_cache.get(target_date):
            return target_workday

        target_workday = next((day for day in self.schedule.days if day.date == target_date), None)
        if not target_workday:
            raise WorkdayNotFoundError(f"Workday {target_date} not found in schedule")

        self._target_workday_cache[target_date] = target_workday

        logger.debug("Found workday for date %s", target_date)
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

    def is_timeslot_available(self, date_str: str, start_time_str: str, end_time_str: str) -> bool:
        """Проверяет, доступен ли заданный промежуток времени."""
        logger.debug("Checking availability for %s %s-%s", date_str, start_time_str, end_time_str)
        start_time = _parse_time_string(start_time_str)
        end_time = _parse_time_string(end_time_str)

        if start_time >= end_time:
            raise InvalidTimeFormatError("Start time must be before end time.")

        target_date = _parse_iso_date_string(date_str).date()
        target_workday = self._get_target_workday(target_date)

        # Проверяем, что время начала и окончания входят в рабочий день
        if not (target_workday.start <= start_time <= end_time <= target_workday.end):
            logger.debug("Timeslot %s-%s is not within the workday for date %s", start_time_str, end_time_str, date_str)
            return False

        busy_time_slots = self.get_busy_time_slots(date_str)

        # Проверяем, что слот не пересекается с занятыми
        return all(not (start_time < slot.end and end_time > slot.start) for slot in busy_time_slots)

    def find_first_available_slot(self, duration_minutes: int) -> list[AvailableTimeSlot]:
        """Находит первое свободное окно для заявки указанной продолжительности."""
        logger.debug("Finding first available slot for %s minutes", duration_minutes)

        # Дата нужна для поддержки вычислений
        dummy_date = datetime.min.replace(tzinfo=UTC).date()

        for day in self.schedule.days:
            if day.date < datetime.now(tz=UTC).date():  # Скипаем прошедшие дни
                logger.debug("Skipping previous date %s", day.date)
                # FIXME В API нет актуальных дат, поэтому имитируем скип
                # continue # noqa: ERA001

            free_slots = self.get_free_timeslots(day.date.isoformat())
            available_slots: list[AvailableTimeSlot] = []

            for slot in free_slots:
                free_slot_start_dt = datetime.combine(dummy_date, slot.start)
                free_slot_end_dt = datetime.combine(dummy_date, slot.end)

                if free_slot_end_dt - free_slot_start_dt >= timedelta(minutes=duration_minutes):
                    available_slots.append(AvailableTimeSlot(date=day.date, start=slot.start, end=slot.end))

            # Зависит от задачи и потребностей, но предположим, что необходимо вернуть окна в ближайшее дате
            if available_slots:
                logger.debug("Found %s available slots on %s: %s", len(available_slots), day.date, available_slots)
                return available_slots

        logger.debug("No available slots found for %s minutes", duration_minutes)
        return []
