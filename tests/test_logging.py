import pytest
import json


from mlserver import ModelSettings
from mlserver.context import model_context
from mlserver.logging import (
    ModelLoggerFormatter,
    configure_logger,
    logger,
    _STREAM_HANDLER_NAME,
)
from mlserver.settings import ModelParameters, Settings
from tests.fixtures import SumModel
from logging import INFO


@pytest.mark.parametrize(
    "name, version, expected_model_fmt, fmt_present_in_all",
    [
        (
            "foo",
            "v1.0",
            "[foo:v1.0]",
            False,
        ),
        (
            "foo",
            "",
            "[foo]",
            False,
        ),
        (
            "",
            "v1.0",
            "",
            True,
        ),
        (
            "",
            "",
            "",
            True,
        ),
    ],
)
def test_model_logging_formatter_unstructured(
    name: str,
    version: str,
    expected_model_fmt: str,
    fmt_present_in_all: bool,
    settings: Settings,
    caplog,
):
    settings.use_structured_logging = False
    caplog.handler.setFormatter(ModelLoggerFormatter(settings))
    caplog.set_level(INFO)

    model_settings = ModelSettings(
        name=name, implementation=SumModel, parameters=ModelParameters(version=version)
    )

    logger.info("Before model context")
    with model_context(model_settings):
        logger.info("Inside model context")
    logger.info("After model context")

    log_records = caplog.get_records("call")
    assert len(log_records) == 3

    assert all(hasattr(lr, "model") for lr in log_records)

    if fmt_present_in_all:
        assert all(lr.model == expected_model_fmt for lr in log_records)
    else:
        assert expected_model_fmt != log_records[0].model
        assert expected_model_fmt == log_records[1].model
        assert expected_model_fmt != log_records[2].model


@pytest.mark.parametrize(
    "name, version, expected_model_fmt, fmt_present_in_all",
    [
        (
            "foo",
            "v1.0",
            ', "model_name": "foo", "model_version": "v1.0"',
            False,
        ),
        (
            "foo",
            "",
            ', "model_name": "foo"',
            False,
        ),
        (
            "",
            "v1.0",
            "",
            True,
        ),
        ("", "", "", True),
    ],
)
def test_model_logging_formatter_structured(
    name: str,
    version: str,
    expected_model_fmt: str,
    fmt_present_in_all: bool,
    settings: Settings,
    caplog,
):
    settings.use_structured_logging = True
    caplog.handler.setFormatter(ModelLoggerFormatter(settings))
    caplog.set_level(INFO)

    model_settings = ModelSettings(
        name=name, implementation=SumModel, parameters=ModelParameters(version=version)
    )

    logger.info("Before model context")
    with model_context(model_settings):
        logger.info("Inside model context")
    logger.info("After model context")

    _ = [json.loads(lr) for lr in caplog.text.strip().split("\n")]
    log_records = caplog.get_records("call")
    assert len(log_records) == 3

    assert all(hasattr(lr, "model") for lr in log_records)

    if fmt_present_in_all:
        assert all(lr.model == expected_model_fmt for lr in log_records)
    else:
        assert expected_model_fmt != log_records[0].model
        assert expected_model_fmt == log_records[1].model
        assert expected_model_fmt != log_records[2].model


@pytest.mark.parametrize("debug", [True, False])
def test_log_level_gets_persisted(debug: bool, settings: Settings, caplog):
    settings.debug = debug
    configure_logger(settings)

    test_log_message = "foo - bar - this is a test"
    logger.debug(test_log_message)

    if debug:
        assert test_log_message in caplog.text
    else:
        assert test_log_message not in caplog.text


def test_configure_logger_when_called_multiple_times_with_same_logger(settings):
    logger = configure_logger()

    assert len(logger.handlers) == 1
    handler = logger.handlers[0]
    assert handler.name == _STREAM_HANDLER_NAME
    assert (
        hasattr(handler.formatter, "use_structured_logging")
        and handler.formatter.use_structured_logging is False
    )

    logger = configure_logger(settings)

    assert len(logger.handlers) == 1
    handler = logger.handlers[0]
    assert handler.name == _STREAM_HANDLER_NAME
    assert (
        hasattr(handler.formatter, "use_structured_logging")
        and handler.formatter.use_structured_logging is False
    )

    settings.use_structured_logging = True
    logger = configure_logger(settings)

    assert len(logger.handlers) == 1
    handler = logger.handlers[0]
    assert handler.name == _STREAM_HANDLER_NAME
    assert (
        hasattr(handler.formatter, "use_structured_logging")
        and handler.formatter.use_structured_logging is True
    )
