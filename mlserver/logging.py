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

_STREAM_HANDLER_NAME = "stdout_stream_handler"


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
    """Log formatter incorporating model details, e.g. name and version."""

    _UNSTRUCTURED_FORMAT = "%(asctime)s [%(name)s]%(model)s %(levelname)s - %(message)s"
    _STRUCTURED_FORMAT = (
        '{"time": "%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", '
        '"message": "%(message)s" %(model)s}'
    )

    def __init__(self, settings: Optional[Settings]):
        self.use_structured_logging = (
            settings is not None and settings.use_structured_logging
        )
        super().__init__(
            self._STRUCTURED_FORMAT
            if self.use_structured_logging
            else self._UNSTRUCTURED_FORMAT
        )

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
        model_details = f', "model_name": "{name}"'
        if version:
            model_details += f', "model_version": "{version}"'
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


def _find_handler(
    logger: logging.Logger, handler_name: str
) -> Optional[logging.Handler]:
    for h in logger.handlers:
        if h.get_name() == handler_name:
            return h
    return None


def configure_logger(settings: Optional[Settings] = None):
    logger = get_logger()

    # Don't add handler twice
    handler = _find_handler(logger, _STREAM_HANDLER_NAME)
    if handler is None:
        handler = StreamHandler(sys.stdout)
        handler.set_name(_STREAM_HANDLER_NAME)
        logger.addHandler(handler)

    handler.setFormatter(ModelLoggerFormatter(settings))

    logger.setLevel(logging.INFO)
    if settings and settings.debug:
        logger.setLevel(logging.DEBUG)

    if settings and settings.logging_settings:
        apply_logging_file(settings.logging_settings)

    return logger
