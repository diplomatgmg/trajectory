from datetime import date, datetime

from pydantic import BaseModel, field_validator


__all__ = [
    "Day",
    "Schedule",
    "TimeSlot",
]


class Day(BaseModel):
    id: int
    date: date
    start: str
    end: str


class TimeSlot(BaseModel):
    id: int
    day_id: int
    start: str
    end: str

    @field_validator("start", "end")
    @classmethod
    def validate_time(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%H:%M")  # noqa: DTZ007
        except ValueError as e:
            raise ValueError("Invalid time format") from e
        return v


class Schedule(BaseModel):
    days: list[Day]
    timeslots: list[TimeSlot]
