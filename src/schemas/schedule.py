from datetime import date

from pydantic import BaseModel

from schemas.common import TimeRangeMixin


__all__ = [
    "Day",
    "FreeTimeSlot",
    "Schedule",
    "TimeSlot",
]


class Day(TimeRangeMixin, BaseModel):
    id: int
    date: date


class TimeSlot(TimeRangeMixin, BaseModel):
    id: int
    day_id: int


class Schedule(BaseModel):
    days: list[Day]
    timeslots: list[TimeSlot]


class FreeTimeSlot(TimeRangeMixin, BaseModel):
    """Модель для представления свободного временного промежутка."""
