import pandas as pd
import numpy as np

from typing import Optional, Any, List, Tuple

from .base import RequestCodec, register_request_codec
from .numpy import to_datatype, to_dtype
from .string import encode_str, StringCodec
from .utils import get_decoded_or_raw, InputOrOutput, inject_batch_dimension
from .lists import ListElement
from ..types import (
    InferenceRequest,
    InferenceResponse,
    RequestInput,
    ResponseOutput,
    Parameters,
)


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
    content_type = None

    if datatype == "BYTES":
        data, content_type = _process_bytes(data, use_bytes)

    shape = inject_batch_dimension(list(series.shape))
    parameters = None
    if content_type:
        parameters = Parameters(content_type=content_type)

    return ResponseOutput(
        name=series.name,
        shape=shape,
        data=data,
        datatype=datatype,
        parameters=parameters,
    )


def _process_bytes(
    data: List[ListElement], use_bytes: bool = True
) -> Tuple[List[ListElement], Optional[str]]:
    # To ensure that "string" columns can be encoded in gRPC, we need to
    # encode them as bytes.
    # We'll also keep track of whether the list should be treated in the
    # future as a list of strings.
    processed = []
    content_type: Optional[str] = StringCodec.ContentType
    for elem in data:
        converted = elem
        if not isinstance(elem, str):
            # There was a non-string element, so we can't determine a content
            # type
            content_type = None
        elif use_bytes:
            converted = encode_str(elem)

        processed.append(converted)

    return processed, content_type


@register_request_codec
class PandasCodec(RequestCodec):
    """
    Decodes a request (response) into a Pandas DataFrame, assuming each input
    (output) head corresponds to a column of the DataFrame.
    """

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
        model_version: Optional[str] = None,
        use_bytes: bool = True,
        **kwargs
    ) -> InferenceResponse:
        outputs = cls.encode_outputs(payload, use_bytes=use_bytes)

        return InferenceResponse(
            model_name=model_name,
            model_version=model_version,
            parameters=Parameters(content_type=cls.ContentType),
            outputs=outputs,
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
            parameters=Parameters(content_type=cls.ContentType),
            inputs=[
                RequestInput(
                    name=output.name,
                    datatype=output.datatype,
                    shape=output.shape,
                    data=output.data,
                    parameters=output.parameters,
                )
                for output in outputs
            ],
        )

    @classmethod
    def decode_request(cls, request: InferenceRequest) -> pd.DataFrame:
        data = {
            request_input.name: _to_series(request_input)
            for request_input in request.inputs
        }

        return pd.DataFrame(data)
