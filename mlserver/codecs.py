import numpy as np

from typing import Any, Dict

from .types import InferenceRequest, InferenceResponse, RequestInput, ResponseOutput

_NP_DTYPES = {
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
    "BYTES": "byte",
}

_DATATYPES_NP = {value: key for key, value in _NP_DTYPES.items()}


class InputCodec:
    """
    The InputCodec interface lets you define type conversions of your raw input
    data to / from the V2 Inference Protocol level.
    Note that this codec applies at the individual input level.
    For request-wide transformations (e.g. dataframes), use the RequestCodec
    interface instead.
    """

    def encode(self, name: str, payload: Any) -> ResponseOutput:
        raise NotImplementedError()

    def decode(self, request_input: RequestInput) -> Any:
        raise NotImplementedError()


class RequestCodec:
    """
    The RequestCodec interface lets you define request-level conversions.
    This can be useful where the encoding of your payload encompases multiple
    input heads (e.g. dataframes).
    For individual input-level encoding / decoding, use the InputCodec
    interface instead.
    """

    def encode(self, name: str, payload: Any) -> InferenceResponse:
        raise NotImplementedError()

    def decode(self, request: InferenceRequest) -> Any:
        raise NotImplementedError()


class _CodecRegistry:
    """
    CodecRegistry is a "fancy" dictionary to register and find codecs.
    This class has a singleton instance exposed at the module leve, which
    should be used preferably.
    """

    def __init__(
        self,
        input_codecs: Dict[str, InputCodec] = {},
        request_codecs: Dict[str, RequestCodec] = {},
    ):
        self._input_codecs = input_codecs
        self._request_codecs = request_codecs

    def register_input_codec(self, content_type: str, codec: InputCodec):
        # TODO: Raise error if codec exists?
        self._input_codecs[content_type] = codec

    def find_input_codec(self, content_type: str) -> InputCodec:
        # TODO: Raise error if codec doesn't exist
        return self._input_codecs[content_type]

    def register_request_codec(self, content_type: str, codec: RequestCodec):
        # TODO: Raise error if codec exists?
        self._request_codecs[content_type] = codec

    def find_request_codec(self, content_type: str) -> RequestCodec:
        # TODO: Raise error if codec doesn't exist
        return self._request_codecs[content_type]


class StringCodec(InputCodec):
    """
    Encodes a Python string as a BYTES input.
    """

    ContentType = "str"
    _str_codec = "utf-8"

    def encode(self, name: str, payload: str) -> ResponseOutput:
        encoded = payload.encode(self._str_codec)

        return ResponseOutput(
            name=name, datatype="BYTES", shape=[len(encoded)], data=encoded
        )

    def decode(self, request_input: RequestInput) -> str:
        encoded = request_input.data.__root__

        if isinstance(encoded, bytes):
            return encoded.decode(self._str_codec)

        if isinstance(encoded, str):
            # NOTE: It may be a string already when decoded from json
            return encoded

        # TODO: Should we raise an error here?
        return ""


class NumpyCodec(InputCodec):
    """
    Encodes a tensor as a numpy array.
    """

    ContentType = "np"

    def encode(self, name: str, payload: np.ndarray) -> ResponseOutput:
        return ResponseOutput(
            name=name,
            datatype=self._to_datatype(payload.dtype),
            shape=list(payload.shape),
            data=payload.flatten().tolist(),
        )

    def decode(self, request_input: RequestInput) -> np.ndarray:
        dtype = self._to_dtype(request_input.datatype)
        data = getattr(request_input.data, "__root__", request_input.data)

        model_data = np.array(data, dtype=dtype)

        # TODO: Check if reshape not valid
        return model_data.reshape(request_input.shape)

    def _to_dtype(self, datatype: str) -> "np.dtype":
        dtype = _NP_DTYPES[datatype]
        return np.dtype(dtype)

    def _to_datatype(self, dtype: np.dtype) -> str:
        as_str = str(dtype)
        datatype = _DATATYPES_NP[as_str]

        return datatype


_codec_registry = _CodecRegistry(
    input_codecs={
        StringCodec.ContentType: StringCodec(),
        NumpyCodec.ContentType: NumpyCodec(),
    }
)
