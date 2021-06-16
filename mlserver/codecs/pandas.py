# TODO: Should we make Pandas optional?
import pandas as pd
import numpy as np

from typing import Any

from .base import RequestCodec, register_request_codec
from .middleware import DecodedParameterName
from ..types import InferenceRequest, InferenceResponse, RequestInput


def _get_decoded_or_raw(request_input: RequestInput) -> Any:
    if request_input.parameters:
        if hasattr(request_input.parameters, DecodedParameterName):
            return getattr(request_input.parameters, DecodedParameterName)

    return request_input.data


def _to_series(request_input: RequestInput) -> pd.Series:
    payload = _get_decoded_or_raw(request_input)
    if isinstance(payload, np.ndarray):
        # Necessary so that it's compatible with pd.Series
        payload = list(payload)

    return pd.Series(payload)


@register_request_codec
class PandasCodec(RequestCodec):
    ContentType = "pd"

    def encode(self, name: str, payload: pd.DataFrame) -> InferenceResponse:
        raise NotImplementedError()

    def decode(self, request: InferenceRequest) -> pd.DataFrame:
        data = {
            request_input.name: _to_series(request_input)
            for request_input in request.inputs
        }

        return pd.DataFrame(data)
