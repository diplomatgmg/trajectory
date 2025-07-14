__all__ = [
    "ScheduleServiceError",
    "WorkdayNotFoundError",
]


class ScheduleServiceError(Exception):
    pass


class WorkdayNotFoundError(ScheduleServiceError):
    """Исключение, возникающее при попытке получить несуществующую дату рабочего дня."""
