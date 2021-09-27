import logging

from .settings import Settings

LoggerName = "mlserver"


def get_logger():
    return logging.getLogger(LoggerName)


def configure_logger(settings: Settings):
    logger = get_logger()
    logger.setLevel(logging.INFO)
    if settings.debug:
        logger.setLevel(logging.DEBUG)

    return logger


logger = get_logger()
