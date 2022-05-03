import logging
import sys

from logging import Formatter, StreamHandler
import logging.config

from .settings import Settings

LoggerName = "mlserver"
LoggerFormat = "%(asctime)s [%(name)s] %(levelname)s - %(message)s"

logger = logging.getLogger(LoggerName)


def get_logger():
    return logger


def apply_logging_file(logging_settings: str):
    logging.config.fileConfig(fname=logging_settings, disable_existing_loggers=False)


def configure_logger(settings: Settings = None):
    logger = get_logger()

    # Don't add handler twice
    if not logger.handlers:
        stream_handler = StreamHandler(sys.stdout)
        formatter = Formatter(LoggerFormat)
        stream_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)

    logger.setLevel(logging.INFO)
    if settings and settings.debug:
        logger.setLevel(logging.DEBUG)

    if settings and settings.logging_settings:
        apply_logging_file(settings.logging_settings)

    return logger
