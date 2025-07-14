__all__ = [
    "InvalidTimeFormatError",
    "ScheduleServiceError",
    "WorkdayNotFoundError",
]


class ScheduleServiceError(Exception):
    pass


class WorkdayNotFoundError(ScheduleServiceError):
    """Исключение, возникающее при попытке получить несуществующую дату рабочего дня."""


class InvalidTimeFormatError(ScheduleServiceError):
    """Неверный формат времени."""
