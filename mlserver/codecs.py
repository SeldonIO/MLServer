import numpy as np

from typing import Any, Dict

from .types import RequestInput, ResponseOutput, TensorData

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


class Codec:
    """
    The Codec interface lets you define type conversions of your raw data to /
    from the V2 Inference Protocol level.
    """

    def encode(self, name: str, payload: Any) -> ResponseOutput:
        raise NotImplementedError()

    def decode(self, request_input: RequestInput) -> Any:
        raise NotImplementedError()


class _CodecRegistry:
    """
    CodecRegistry is a "fancy" dictionary to register and find codecs.
    This class has a singleton instance exposed at the module leve, which
    should be used preferably.
    """

    def __init__(self, codecs: Dict[str, Codec] = {}):
        self._codecs = codecs

    def register(self, name: str, codec: Codec):
        # TODO: Raise error if codec exists?
        self._codecs[name] = codec

    def find_codec(self, name: str) -> Codec:
        # TODO: Raise error if codec doesn't exist
        return self._codecs[name]


class StringCodec(Codec):
    """
    Encodes a Python string as a BYTES input.
    """

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


class NumpyCodec(Codec):
    """
    Encodes a tensor as a numpy array.
    """

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


_codec_registry = _CodecRegistry({"str": StringCodec(), "np": NumpyCodec()})
