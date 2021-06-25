import pytest

from mlserver.model import MLModel
from mlserver.handlers.custom import CustomHandlerRegistry, CustomHandler


@pytest.fixture
def custom_handler_registry() -> CustomHandlerRegistry:
    return CustomHandlerRegistry()


@pytest.fixture
def custom_handler(sum_model: MLModel) -> CustomHandler:
    def my_custom_path(payload: dict) -> dict:
        return {"foo": "bar"}

    return CustomHandler(
        rest_path="/my-custom-path", runtime=sum_model.__class__, handler=my_custom_path
    )
