import logging
import sys

from logging import Formatter, StreamHandler

from .settings import Settings

LoggerName = "mlserver"
LoggerFormat = "%(asctime)s [%(name)s] %(levelname)s - %(message)s"

logger = logging.getLogger(LoggerName)


def get_logger():
    return logger


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

    return logger
