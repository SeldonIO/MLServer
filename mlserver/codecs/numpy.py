import numpy as np

from typing import Any, Union

from ..types import RequestInput, ResponseOutput

from .base import InputCodec, register_input_codec, register_request_codec
from .utils import FirstInputRequestCodec

_DatatypeToNumpy = {
    "BOOL": "bool",
    "UINT8": "uint8",
    "UINT16": "uint16",
    "UINT32": "uint32",
    "UINT64": "uint64",
    "INT8": "int8",
    "INT16": "int16",
    "INT32": "int32",
    "INT64": "int64",
    "FP16": "float16",
    "FP32": "float32",
    "FP64": "float64",
    "BYTES": "bytes",
}

_NumpyToDatatype = {value: key for key, value in _DatatypeToNumpy.items()}

# NOTE: numpy has more types than v2 protocol
_NumpyToDatatype["object"] = "BYTES"
_NumpyToDatatype["S"] = "BYTES"


def _to_dtype(v2_data: Union[RequestInput, ResponseOutput]) -> "np.dtype":
    dtype = _DatatypeToNumpy[v2_data.datatype]

    if v2_data.datatype == "BYTES":
        # bytes have variable size, so need to specify as part of type
        # TODO: Make elem size variable (and not just the last dimension)
        elem_size = v2_data.shape[-1]
        return np.dtype((dtype, elem_size))

    return np.dtype(dtype)


def to_datatype(dtype: np.dtype) -> str:
    as_str = str(dtype)

    if as_str not in _NumpyToDatatype:
        # If not present, try with kind
        as_str = getattr(dtype, "kind")

    datatype = _NumpyToDatatype[as_str]

    return datatype


def _to_ndarray(v2_data: Union[RequestInput, ResponseOutput]) -> np.ndarray:
    data = getattr(v2_data.data, "__root__", v2_data.data)
    dtype = _to_dtype(v2_data)

    if v2_data.datatype == "BYTES":
        return np.frombuffer(data, dtype)

    return np.array(data, dtype)


def _encode_data(data: np.ndarray, datatype: str) -> Any:
    if datatype == "BYTES":
        # tobytes is way faster than tolist, although it's harder to serialise
        # and only makes sense for actual bytes inputs (#253)
        return data.tobytes()

    return data.flatten().tolist()


@register_input_codec
class NumpyCodec(InputCodec):
    """
    Encodes a tensor as a numpy array.
    """

    ContentType = "np"

    @classmethod
    def encode(cls, name: str, payload: np.ndarray) -> ResponseOutput:
        datatype = to_datatype(payload.dtype)

        return ResponseOutput(
            name=name,
            datatype=datatype,
            shape=list(payload.shape),
            data=_encode_data(payload, datatype),
        )

    @classmethod
    def decode(cls, v2_data: RequestInput) -> np.ndarray:
        model_data = _to_ndarray(v2_data)

        # TODO: Check if reshape not valid
        return model_data.reshape(v2_data.shape)

    @classmethod
    def decode_response_output(cls, v2_data: ResponseOutput) -> np.ndarray:
        # TODO: merge this logic with `decode`
        model_data = _to_ndarray(v2_data)

        # TODO: Check if reshape not valid
        return model_data.reshape(v2_data.shape)

    @classmethod
    def encode_request_input(cls, name: str, payload: np.ndarray, enable_quantize: bool = False) -> RequestInput:
        # TODO: merge this logic with `encode`
        datatype = to_datatype(payload.dtype)

        if enable_quantize:
            # we quantize to FP32
            if datatype == "FP64":
                datatype = "FP32"
            elif datatype == "INT64":
                datatype = "INT32"
            elif datatype == "UINT64":
                datatype = "UINT32"

        return RequestInput(
            name=name,
            datatype=datatype,
            shape=list(payload.shape),
            data=_encode_data(payload, datatype),
        )


@register_request_codec
class NumpyRequestCodec(FirstInputRequestCodec):
    InputCodec = NumpyCodec
    ContentType = NumpyCodec.ContentType
