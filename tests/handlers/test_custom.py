from mlserver.handlers.custom import (
    _CustomHandlerAttr,
    CustomHandler,
    get_custom_handlers,
)

from ..fixtures import SumModel


def test_custom_handler(sum_model: SumModel, custom_handler: CustomHandler):
    assert hasattr(sum_model.my_payload, _CustomHandlerAttr)
    assert getattr(sum_model.my_payload, _CustomHandlerAttr) == custom_handler


def test_get_custom_handlers(sum_model: SumModel, custom_handler: CustomHandler):
    handlers = get_custom_handlers(sum_model)

    # NOTE: The first handler is the "test" handler used to test large response
    # payloads (e.g. to validate compression is working as expected)
    assert len(handlers) == 2
    assert handlers[1] == (custom_handler, sum_model.my_payload)
