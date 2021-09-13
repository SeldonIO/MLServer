import inspect

from typing import Tuple, Any, Callable, List
from pydantic import BaseModel

from ..model import MLModel

_CustomHandlerAttr = "__custom_handler__"
_HandlerMethod = Callable[..., Any]


class CustomHandler(BaseModel):
    rest_path: str
    rest_method: str = "POST"


def custom_handler(rest_path: str, rest_method: str = "POST"):
    def _wraps(f):
        handler = CustomHandler(rest_path=rest_path, rest_method=rest_method)
        setattr(f, _CustomHandlerAttr, handler)
        return f

    return _wraps


def get_custom_handlers(model: MLModel) -> List[Tuple[CustomHandler, _HandlerMethod]]:
    handlers = []
    members = inspect.getmembers(model)

    for _, member in members:
        if not hasattr(member, _CustomHandlerAttr):
            continue

        custom_handler = getattr(member, _CustomHandlerAttr)
        handlers.append((custom_handler, member))

    return handlers
