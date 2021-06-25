from mlserver.model import MLModel
from mlserver.handlers.custom import CustomHandlerRegistry, CustomHandler


def test_register_custom_handler(
    custom_handler_registry: CustomHandlerRegistry,
    custom_handler: CustomHandler,
    sum_model: MLModel,
):
    custom_handler_registry.register_handler(custom_handler)

    assert len(custom_handler_registry._handlers) == 1
    assert sum_model.__class__ in custom_handler_registry._handlers
    assert len(custom_handler_registry._handlers[sum_model.__class__]) == 1
    assert custom_handler_registry._handlers[sum_model.__class__][0] == custom_handler
