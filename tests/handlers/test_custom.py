from mlserver.model import MLModel
from mlserver.handlers.custom import CustomHandlerRegistry, CustomHandler


def test_register_handler(
    custom_handler_registry: CustomHandlerRegistry,
    custom_handler: CustomHandler,
    sum_model: MLModel,
):
    new_custom_handler = CustomHandler(
        rest_path="/new-path",
        runtime=sum_model.__class__,
        handler=custom_handler.handler,
    )

    custom_handler_registry.register_handler(new_custom_handler)

    assert len(custom_handler_registry._handlers) == 1
    assert sum_model.__class__ in custom_handler_registry._handlers
    assert len(custom_handler_registry._handlers[sum_model.__class__]) == 2
    assert custom_handler_registry._handlers[sum_model.__class__] == [
        custom_handler,
        new_custom_handler,
    ]


def test_find_handlers(
    custom_handler_registry: CustomHandlerRegistry,
    custom_handler: CustomHandler,
    sum_model: MLModel,
):
    handlers = custom_handler_registry.find_handlers(sum_model.__class__)

    assert handlers == [custom_handler]


def test_find_handlers_empty(
    custom_handler_registry: CustomHandlerRegistry,
):
    handlers = custom_handler_registry.find_handlers(MLModel)

    assert len(handlers) == 0
