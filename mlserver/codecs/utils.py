from typing import Any

from .middleware import DecodedParameterName


def get_decoded_or_raw(parametrised_obj) -> Any:
    if parametrised_obj.parameters:
        if hasattr(parametrised_obj.parameters, DecodedParameterName):
            return getattr(parametrised_obj.parameters, DecodedParameterName)

    if hasattr(parametrised_obj, "data"):
        # If this is a RequestInput, return its data
        return parametrised_obj.data

    # Otherwise, return full object
    return parametrised_obj
