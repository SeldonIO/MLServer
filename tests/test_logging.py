import pytest

from mlserver.logging import logger, configure_logger
from mlserver.settings import Settings


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
