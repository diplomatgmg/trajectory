from datetime import datetime

from pydantic import BaseModel, field_validator


__all__ = ["ScheduleResponse"]


class Day(BaseModel):
    id: int
    date: str
    start: str
    end: str

    @field_validator("date")
    @classmethod
    def validate_date(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d")  # noqa: DTZ007
        except ValueError as e:
            raise ValueError("Invalid date format") from e
        return v

    @field_validator("start", "end")
    @classmethod
    def validate_time(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%H:%M")  # noqa: DTZ007
        except ValueError as e:
            raise ValueError("Invalid time format") from e
        return v


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


class ScheduleResponse(BaseModel):
    days: list[Day]
    timeslots: list[TimeSlot]
