import pandas as pd
import numpy as np

from typing import Any, List

from .base import RequestCodec, register_request_codec
from .numpy import to_datatype, to_dtype
from .string import encode_str
from .utils import get_decoded_or_raw
from .pack import PackElement
from ..types import InferenceRequest, InferenceResponse, RequestInput, ResponseOutput


def _to_series(request_input: RequestInput) -> pd.Series:
    payload = get_decoded_or_raw(request_input)
    if isinstance(payload, np.ndarray):
        # Necessary so that it's compatible with pd.Series
        payload = list(payload)
        dtype = to_dtype(request_input)
        return pd.Series(payload, dtype=dtype)

    return pd.Series(payload)


def _to_response_output(series: pd.Series) -> ResponseOutput:
    datatype = to_datatype(series.dtype)
    data = series.tolist()

    if datatype == "BYTES":
        # To ensure that "string" columns can be encoded in gRPC, we need to
        # encode them as bytes
        data = list(map(_ensure_bytes, data))

    return ResponseOutput(
        name=series.name,
        shape=list(series.shape),
        # If string, it should be encoded to bytes
        data=data,
        datatype=datatype,
    )


def _ensure_bytes(elem: PackElement) -> bytes:
    if isinstance(elem, str):
        return encode_str(elem)

    return elem


@register_request_codec
class PandasCodec(RequestCodec):
    ContentType = "pd"

    @classmethod
    def can_encode(cls, payload: Any) -> bool:
        return isinstance(payload, pd.DataFrame)

    @classmethod
    def encode(
        cls, model_name: str, payload: pd.DataFrame, model_version: str = None
    ) -> InferenceResponse:
        outputs = cls.encode_outputs(payload)

        return InferenceResponse(
            model_name=model_name, model_version=model_version, outputs=outputs
        )

    @classmethod
    def encode_outputs(cls, payload: pd.DataFrame) -> List[ResponseOutput]:
        return [_to_response_output(payload[col]) for col in payload]

    @classmethod
    def decode(cls, request: InferenceRequest) -> pd.DataFrame:
        data = {
            request_input.name: _to_series(request_input)
            for request_input in request.inputs
        }

        return pd.DataFrame(data)
