from typing import Any

from ..types import RequestInput
from .middleware import DecodedParameterName


def get_decoded_or_raw(request_input: RequestInput) -> Any:
    if request_input.parameters:
        if hasattr(request_input.parameters, DecodedParameterName):
            return getattr(request_input.parameters, DecodedParameterName)

    return request_input.data
