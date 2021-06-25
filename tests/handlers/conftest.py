import pytest

from mlserver.model import MLModel
from mlserver.handlers.custom import CustomHandlerRegistry, CustomHandler


@pytest.fixture
def custom_handler(sum_model: MLModel) -> CustomHandler:
    def my_custom_path(payload: dict) -> dict:
        return {"foo": "bar"}

    return CustomHandler(
        rest_path="/my-custom-path", runtime=sum_model.__class__, handler=my_custom_path
    )


@pytest.fixture
def custom_handler_registry(custom_handler: CustomHandler) -> CustomHandlerRegistry:
    reg = CustomHandlerRegistry()
    reg.register_handler(custom_handler)

    return reg
