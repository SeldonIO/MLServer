import pandas as pd
import numpy as np

from typing import Any, List

from .base import RequestCodec, register_request_codec
from .numpy import to_datatype, to_dtype
from .string import encode_str
from .utils import get_decoded_or_raw, InputOrOutput
from .lists import ListElement
from ..types import InferenceRequest, InferenceResponse, RequestInput, ResponseOutput


def _to_series(input_or_output: InputOrOutput) -> pd.Series:
    payload = get_decoded_or_raw(input_or_output)

    if input_or_output.datatype == "BYTES":
        # Don't convert the dtype of BYTES
        return pd.Series(payload)

    if isinstance(payload, np.ndarray):
        # Necessary so that it's compatible with pd.Series
        payload = list(payload)

    dtype = to_dtype(input_or_output)
    return pd.Series(payload, dtype=dtype)


def _to_response_output(series: pd.Series, use_bytes: bool = True) -> ResponseOutput:
    datatype = to_datatype(series.dtype)
    data = series.tolist()

    if datatype == "BYTES" and use_bytes:
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


def _ensure_bytes(elem: ListElement) -> bytes:
    if isinstance(elem, str):
        return encode_str(elem)

    return elem


@register_request_codec
class PandasCodec(RequestCodec):
    ContentType = "pd"
    TypeHint = pd.DataFrame

    @classmethod
    def can_encode(cls, payload: Any) -> bool:
        return isinstance(payload, pd.DataFrame)

    @classmethod
    def encode_response(
        cls,
        model_name: str,
        payload: pd.DataFrame,
        model_version: str = None,
        use_bytes: bool = True,
        **kwargs
    ) -> InferenceResponse:
        outputs = cls.encode_outputs(payload, use_bytes=use_bytes)

        return InferenceResponse(
            model_name=model_name, model_version=model_version, outputs=outputs
        )

    @classmethod
    def decode_response(cls, response: InferenceResponse) -> pd.DataFrame:
        data = {
            response_output.name: _to_series(response_output)
            for response_output in response.outputs
        }

        return pd.DataFrame(data)

    @classmethod
    def encode_outputs(
        cls, payload: pd.DataFrame, use_bytes: bool = True
    ) -> List[ResponseOutput]:
        return [
            _to_response_output(payload[col], use_bytes=use_bytes) for col in payload
        ]

    @classmethod
    def encode_request(
        cls, payload: pd.DataFrame, use_bytes: bool = True, **kwargs
    ) -> InferenceRequest:
        outputs = cls.encode_outputs(payload, use_bytes=use_bytes)

        return InferenceRequest(
            inputs=[
                RequestInput(
                    name=output.name,
                    datatype=output.datatype,
                    shape=output.shape,
                    data=output.data,
                )
                for output in outputs
            ]
        )

    @classmethod
    def decode_request(cls, request: InferenceRequest) -> pd.DataFrame:
        data = {
            request_input.name: _to_series(request_input)
            for request_input in request.inputs
        }

        return pd.DataFrame(data)
