import pytest

from mlserver.handlers.custom import CustomHandler


@pytest.fixture
def custom_handler() -> CustomHandler:
    return CustomHandler(rest_path="/my-custom-endpoint")
