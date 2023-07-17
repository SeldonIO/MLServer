import pytest

from mlserver import ModelSettings
from mlserver.context import model_context
from mlserver.logging import ModelLoggerFormatter, LoggerFormat
from mlserver.settings import ModelParameters
from tests.fixtures import SumModel
from logging import getLogger, INFO


logger = getLogger("test.formatter")


@pytest.mark.parametrize(
    "name, version, expected_fmt",
    [
        (
            "foo",
            "v1.0",
            "[foo:v1.0]",
        ),
        (
            "foo",
            "",
            "[foo]",
        ),
        (
            "foo",
            None,
            "[foo]",
        ),
    ],
)
def test_model_logging_formatter(caplog, name, version, expected_fmt):
    caplog.handler.setFormatter(ModelLoggerFormatter(LoggerFormat))
    caplog.set_level(INFO)

    model_settings = ModelSettings(
        name=name, implementation=SumModel, parameters=ModelParameters(version=version)
    )

    logger.info("Before model context")
    with model_context(model_settings):
        logger.info(f"Inside model context")
    logger.info("After model context")

    log_records = caplog.text.strip().split("\n")
    assert len(caplog.messages) == 3

    assert expected_fmt not in log_records[0]
    assert expected_fmt in log_records[1]
    assert expected_fmt not in log_records[2]
