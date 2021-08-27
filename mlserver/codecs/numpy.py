import numpy as np

from typing import Any

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


def _to_dtype(request_input: RequestInput) -> "np.dtype":
    dtype = _DatatypeToNumpy[request_input.datatype]

    if request_input.datatype == "BYTES":
        # bytes have variable size, so need to specify as part of type
        # TODO: Make elem size variable (and not just the last dimension)
        elem_size = request_input.shape[-1]
        return np.dtype((dtype, elem_size))

    return np.dtype(dtype)


def _to_datatype(dtype: np.dtype) -> str:
    as_str = str(dtype)

    if as_str not in _NumpyToDatatype:
        # If not present, try with kind
        as_str = getattr(dtype, "kind")

    datatype = _NumpyToDatatype[as_str]

    return datatype


def _to_ndarray(request_input: RequestInput) -> np.ndarray:
    data = getattr(request_input.data, "__root__", request_input.data)
    dtype = _to_dtype(request_input)

    if request_input.datatype == "BYTES":
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
        datatype = _to_datatype(payload.dtype)

        return ResponseOutput(
            name=name,
            datatype=datatype,
            shape=list(payload.shape),
            data=_encode_data(payload, datatype),
        )

    @classmethod
    def decode(cls, request_input: RequestInput) -> np.ndarray:
        model_data = _to_ndarray(request_input)

        # TODO: Check if reshape not valid
        return model_data.reshape(request_input.shape)


@register_request_codec
class NumpyRequestCodec(FirstInputRequestCodec):
    InputCodec = NumpyCodec
    ContentType = NumpyCodec.ContentType
