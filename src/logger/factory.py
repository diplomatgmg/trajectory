import logging

from logger.config import log_config


__all__ = ["setup_logger"]


def setup_logger() -> None:
    """Инициализирует логгер для модуля."""
    logging.basicConfig(
        level=log_config.level.value,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
