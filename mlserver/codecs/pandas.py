# TODO: Should we make Pandas optional?
import pandas as pd
import numpy as np

from .base import RequestCodec, register_request_codec
from .numpy import _to_datatype
from .utils import get_decoded_or_raw
from ..types import InferenceRequest, InferenceResponse, RequestInput, ResponseOutput


def _to_series(request_input: RequestInput) -> pd.Series:
    payload = get_decoded_or_raw(request_input)
    if isinstance(payload, np.ndarray):
        # Necessary so that it's compatible with pd.Series
        payload = list(payload)

    return pd.Series(payload)


def _to_response_output(series: pd.Series) -> ResponseOutput:
    return ResponseOutput(
        name=series.name,
        shape=list(series.shape),
        data=series.tolist(),
        datatype=_to_datatype(series.dtype),
    )


@register_request_codec
class PandasCodec(RequestCodec):
    ContentType = "pd"

    @classmethod
    def encode(
        cls, model_name: str, payload: pd.DataFrame, model_version: str = None
    ) -> InferenceResponse:
        outputs = [_to_response_output(payload[col]) for col in payload]

        return InferenceResponse(
            model_name=model_name, model_version=model_version, outputs=outputs
        )

    @classmethod
    def decode(cls, request: InferenceRequest) -> pd.DataFrame:
        data = {
            request_input.name: _to_series(request_input)
            for request_input in request.inputs
        }

        return pd.DataFrame(data)
