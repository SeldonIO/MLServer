import json
import logging
import sys

from logging import StreamHandler
from pathlib import Path
from typing import Optional, Dict, Union
import logging.config

from .context import model_name_var, model_version_var
from .settings import Settings

LoggerName = "mlserver"

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


class ModelLoggerFormatter(logging.Formatter):
    """
    A logging formatter that uses context variables to inject
    the model name and version in the log message.
    """

    _UNSTRUCTURED_FORMAT = "%(asctime)s [%(name)s]%(model)s %(levelname)s - %(message)s"
    _STRUCTURED_FORMAT = "{\"time\":\"%(asctime)s\", \"name\": \"%(name)s\", " \
                         "\"level\": \"%(levelname)s\", \"message\": \"%(message)s\"" \
                         " %(model)s}"

    def __init__(self, use_structured_logging: bool):
        super().__init__(
            self._STRUCTURED_FORMAT
            if use_structured_logging
            else self._UNSTRUCTURED_FORMAT
        )
        self.use_structured_logging = use_structured_logging

    @staticmethod
    def _format_unstructured_model_details(name: str, version: str) -> str:
        if not name:
            return ""
        elif not version:
            return f"[{name}]"
        else:
            return f"[{name}:{version}]"

    @staticmethod
    def _format_structured_model_details(name: str, version: str) -> str:
        if not name:
            return ""
        model_details = f", \"model_name\": \"{name}\""
        if version:
            model_details += f", \"model_version\": \"{version}\""
        return model_details

    def format(self, record: logging.LogRecord) -> str:
        model_name = model_name_var.get("")
        model_version = model_version_var.get("")

        record.model = (
            self._format_structured_model_details(model_name, model_version)
            if self.use_structured_logging
            else self._format_unstructured_model_details(model_name, model_version)
        )

        return super().format(record)


def configure_logger(settings: Optional[Settings] = None):
    logger = get_logger()

    # Don't add handler twice
    if not logger.handlers:
        stream_handler = StreamHandler(sys.stdout)

        use_structured_logging = False
        if settings and settings.use_structured_logging:
            use_structured_logging = True

        formatter = ModelLoggerFormatter(use_structured_logging)
        stream_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)

    logger.setLevel(logging.INFO)
    if settings and settings.debug:
        logger.setLevel(logging.DEBUG)

    if settings and settings.logging_settings:
        apply_logging_file(settings.logging_settings)

    return logger
