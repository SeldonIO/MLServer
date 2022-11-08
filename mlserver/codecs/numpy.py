import numpy as np

from typing import Any

from ..types import RequestInput, ResponseOutput, Parameters

from .base import InputCodec, register_input_codec, register_request_codec
from .utils import SingleInputRequestCodec, InputOrOutput, inject_batch_dimension
from .lists import is_list_of
from .string import encode_str

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
_NumpyToDatatype["U"] = "BYTES"


def to_dtype(input_or_output: InputOrOutput) -> "np.dtype":
    dtype = _DatatypeToNumpy[input_or_output.datatype]

    if input_or_output.datatype == "BYTES":
        data = getattr(input_or_output.data, "__root__", input_or_output.data)
        if is_list_of(data, str):
            # Handle special case of strings being treated as Numpy arrays
            return np.dtype(str)

        # bytes have variable size, so need to specify as part of type
        # TODO: Make elem size variable (and not just the last dimension)
        elem_size = input_or_output.shape[-1]
        return np.dtype((dtype, elem_size))

    return np.dtype(dtype)


def to_datatype(dtype: np.dtype) -> str:
    as_str = str(dtype)

    if as_str not in _NumpyToDatatype:
        # If not present, try with kind
        as_str = getattr(dtype, "kind")

    datatype = _NumpyToDatatype[as_str]

    return datatype


def _to_ndarray(input_or_output: InputOrOutput) -> np.ndarray:
    data = getattr(input_or_output.data, "__root__", input_or_output.data)
    dtype = to_dtype(input_or_output)

    if input_or_output.datatype == "BYTES":
        if is_list_of(data, bytes):
            # If the inputs is of type `BYTES`, there could be multiple "lists"
            # serialised into multiple buffers.
            # We will deserialise all of them and concatenate them together.
            decoded = [np.frombuffer(buffer, dtype) for buffer in data]
            return np.concatenate(decoded)

    return np.array(data, dtype)


def _encode_data(data: np.ndarray, datatype: str) -> list:
    if datatype == "BYTES":
        if np.issubdtype(data.dtype, str):
            # Handle special case of a string Numpy array, where the diff elems
            # need to be encoded as well
            as_list = data.flatten().tolist()
            return list(map(encode_str, as_list))

        if np.issubdtype(data.dtype, bytes):
            # `tobytes` is way faster than tolist, although it's harder to serialise
            # and only makes sense for actual bytes inputs (#253).
            # Note that `.tobytes()` will return a single `bytes` payload, thus we
            # need to encapsulate it into a list so that it's compatible.
            return [data.tobytes()]

    return data.flatten().tolist()


@register_input_codec
class NumpyCodec(InputCodec):
    """
    Encodes a tensor as a numpy array.
    """

    ContentType = "np"
    TypeHint = np.ndarray

    @classmethod
    def can_encode(csl, payload: Any) -> bool:
        return isinstance(payload, np.ndarray)

    @classmethod
    def encode_output(cls, name: str, payload: np.ndarray, **kwargs) -> ResponseOutput:
        datatype = to_datatype(payload.dtype)

        shape = inject_batch_dimension(list(payload.shape))

        return ResponseOutput(
            name=name,
            datatype=datatype,
            shape=shape,
            data=_encode_data(payload, datatype),
        )

    @classmethod
    def decode_output(cls, response_output: ResponseOutput) -> np.ndarray:
        return cls.decode_input(response_output)  # type: ignore

    @classmethod
    def encode_input(cls, name: str, payload: np.ndarray, **kwargs) -> RequestInput:
        output = cls.encode_output(name=name, payload=payload)

        return RequestInput(
            name=output.name,
            datatype=output.datatype,
            shape=output.shape,
            data=output.data,
            parameters=Parameters(content_type=cls.ContentType),
        )

    @classmethod
    def decode_input(cls, request_input: RequestInput) -> np.ndarray:
        model_data = _to_ndarray(request_input)

        # TODO: Check if reshape not valid
        return model_data.reshape(request_input.shape)


@register_request_codec
class NumpyRequestCodec(SingleInputRequestCodec):
    InputCodec = NumpyCodec
    ContentType = NumpyCodec.ContentType
