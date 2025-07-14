from datetime import time

import pytest

from schemas.schedule import FreeTimeSlot


def test_time_range_valid_creation() -> None:
    """Тест на успешное создание объекта, когда время начала раньше времени окончания."""
    slot = FreeTimeSlot(start=time(9, 0), end=time(10, 30))

    assert slot.start == time(9, 0)
    assert slot.end == time(10, 30)


@pytest.mark.parametrize(
    ("start_time", "end_time"),
    [
        pytest.param(time(10, 0), time(9, 0), id="start_after_end"),  # Начало > Окончания
        pytest.param(time(12, 30), time(12, 30), id="start_equals_end"),  # Начало == Окончанию
    ],
)
def test_time_range_invalid_creation(start_time: time, end_time: time) -> None:
    """Тест на ошибку валидации, когда время начала >= времени окончания."""
    with pytest.raises(ValueError) as exc_info:  # noqa: PT011 Жалуется что ValueError общее исключение, так и надо.
        FreeTimeSlot(start=start_time, end=end_time)

    expected_error = f"Время начала '{start_time}' должно быть больше времени окончания '{end_time}'"
    assert expected_error in str(exc_info.value)
