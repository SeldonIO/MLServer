from typing import Callable

from fastapi import status
from fastapi.routing import APIRoute
from starlette.types import Scope

from ..handlers.custom import CustomHandler


def to_status_code(flag: bool, error_code: int = status.HTTP_400_BAD_REQUEST) -> int:
    """
    Convert a boolean flag into a HTTP status code.
    """
    if flag:
        return status.HTTP_200_OK

    return error_code


def matches(
    route: APIRoute, custom_handler: CustomHandler, handler_method: Callable
) -> bool:
    if route.endpoint != handler_method:
        return False

    scope = to_scope(custom_handler)
    match, _ = route.matches(scope)
    if match == match.NONE:
        return False

    return True


def to_scope(custom_handler: CustomHandler) -> Scope:
    return {
        "type": "http",
        "method": custom_handler.rest_method,
        "path": custom_handler.rest_path,
    }
