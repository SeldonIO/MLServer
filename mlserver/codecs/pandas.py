# TODO: Should we make Pandas optional?
import pandas as pd

from typing import Any

from .base import RequestCodec, register_request_codec
from .middleware import DecodedParameterName
from ..types import InferenceRequest, InferenceResponse, RequestInput


def _get_decoded_or_raw(request_input: RequestInput) -> Any:
    if request_input.parameters:
        if hasattr(request_input.parameters, DecodedParameterName):
            return getattr(request_input.parameters, DecodedParameterName)

    return request_input.data


@register_request_codec
class PandasCodec(RequestCodec):
    ContentType = "pd"

    def encode(self, name: str, payload: pd.DataFrame) -> InferenceResponse:
        raise NotImplementedError()

    def decode(self, request: InferenceRequest) -> pd.DataFrame:
        data = {
            request_input.name: _get_decoded_or_raw(request_input)
            for request_input in request.inputs
        }
        breakpoint()
        return pd.DataFrame(data)
