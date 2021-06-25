from typing import Any, Callable, Dict, List, Type
from pydantic import BaseModel

from ..model import MLModel

_Handler = Callable[..., Any]
_HandlerDict = Dict[Type[MLModel], List["CustomHandler"]]


class CustomHandler(BaseModel):
    rest_path: str
    runtime: Type[MLModel]
    handler: _Handler


class CustomHandlerRegistry:
    def __init__(self):
        self._handlers: _HandlerDict = {}

    def register_handler(self, custom_handler: CustomHandler):
        if custom_handler.runtime not in self._handlers:
            self._handlers[custom_handler.runtime] = []

        # TODO: Do we need to check for duplicates?
        self._handlers[custom_handler.runtime].append(custom_handler)

    def find_handlers(self, runtime: Type[MLModel]) -> List[CustomHandler]:
        if runtime not in self._handlers:
            return []

        return self._handlers[runtime]
