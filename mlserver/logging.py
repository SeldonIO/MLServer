import json
import logging
import sys

from logging import Formatter, StreamHandler
from pathlib import Path
from typing import Optional, Dict, Union
import logging.config

from .settings import Settings

LoggerName = "mlserver"
LoggerFormat = "%(asctime)s [%(name)s] %(levelname)s - %(message)s"

logger = logging.getLogger(LoggerName)


def get_logger():
    return logger


def apply_logging_file(logging_settings: Union[str, Dict]):
    if isinstance(logging_settings, str) and Path(logging_settings).is_file():
        if "json" in Path(logging_settings).suffix:
            with open(logging_settings) as settings_file:
                config = json.load(settings_file)
            logging.config.dictConfig(config)
        else:
            logging.config.fileConfig(
                fname=logging_settings, disable_existing_loggers=False
            )
    elif isinstance(logging_settings, Dict):
        logging.config.dictConfig(logging_settings)
    else:
        logger.warning("Unable to parse logging_settings.")


def configure_logger(settings: Optional[Settings] = None):
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
