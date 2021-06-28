from fastapi import status
from starlette.types import Scope

from ..handlers.custom import CustomHandler


def to_status_code(flag: bool, error_code: int = status.HTTP_400_BAD_REQUEST) -> int:
    """
    Convert a boolean flag into a HTTP status code.
    """
    if flag:
        return status.HTTP_200_OK

    return error_code


def to_scope(custom_handler: CustomHandler) -> Scope:
    return {
        "type": "http",
        "method": custom_handler.rest_method,
        "path": custom_handler.rest_path,
    }
