import pytest

from mlserver.handlers.custom import CustomHandler

from ..fixtures import SumModel


@pytest.fixture
def custom_handler(sum_model: SumModel) -> CustomHandler:
    return CustomHandler(rest_path="/my-custom-endpoint")
