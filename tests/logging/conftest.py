import logging
import pytest

from mlserver.logging import ModelLoggerFormatter, LoggerFormat


# @pytest.fixture(autouse=True)
# def caplog_with_model_logger_formatter(caplog):
#     caplog.handler.setFormatter(ModelLoggerFormatter(LoggerFormat))
#     caplog.set_level(logging.INFO)
