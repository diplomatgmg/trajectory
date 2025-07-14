from datetime import time
from typing import Self

from pydantic import model_validator


__all__ = ["TimeRangeMixin"]


class TimeRangeMixin:
    start: time
    end: time

    @model_validator(mode="after")
    def check_start_before_end(self) -> Self:
        """Проверяет, что время начала раньше времени окончания."""
        if self.start >= self.end:
            raise ValueError(f"Время начала '{self.start}' должно быть больше времени окончания '{self.end}'")
        return self
