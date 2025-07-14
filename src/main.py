import logging

from httpx import AsyncClient
import uvloop

from clients.schedule import ScheduleClient
from logger.factory import setup_logger
from services.schedule import ScheduleService


setup_logger()

logger = logging.getLogger(__name__)


async def main() -> None:
    async with AsyncClient() as client:
        schedule_client = ScheduleClient(client)
        schedules = await schedule_client.get_schedules()

    schedule_service = ScheduleService(schedules)

    # Тут может быть поддержка командной строки, или это api сервис.
    # Оставил просто пример, чтобы не было лишнего кода

    busy_date = "2025-02-18"
    logger.info("Finding busy slots for %s", busy_date)

    # Занятые Окна
    busy_slots = schedule_service.get_busy_time_slots(busy_date)
    for busy_slot in busy_slots:
        logger.info("Busy slot: start=%s, end=%s", busy_slot.start, busy_slot.end)

    free_date = "2025-02-18"
    logger.info("Finding free slots for %s", free_date)

    # Свободные Окна
    free_slots = schedule_service.get_free_timeslots(free_date)
    for free_slot in free_slots:
        logger.info("Free slot: start=%s, end=%s", free_slot.start, free_slot.end)

    # Ближайшее окно
    duration = 30
    logger.info("Finding available slots for %s minutes", duration)

    available_slots = schedule_service.find_first_available_slot(duration)
    for available_slot in available_slots:
        logger.info(
            "Available slot: date=%s, start=%s, end=%s", available_slot.date, available_slot.start, available_slot.end
        )


if __name__ == "__main__":
    uvloop.run(main())
