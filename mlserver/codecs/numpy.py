import numpy as np

from ..types import InferenceRequest, InferenceResponse, RequestInput, ResponseOutput

from .base import RequestCodec, InputCodec, register_input_codec, register_request_codec

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
    "BYTES": "byte",
}

_NumpyToDatatype = {value: key for key, value in _DatatypeToNumpy.items()}

ContentType = "np"


@register_request_codec(ContentType)
class NumpyRequestCodec(RequestCodec):
    """
    Encodes a multiple-input request as a NumPy tensor.
    """

    ContentType = ContentType

    pass


@register_input_codec(ContentType)
class NumpyCodec(InputCodec):
    """
    Encodes a tensor as a numpy array.
    """

    ContentType = ContentType

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
        dtype = _DatatypeToNumpy[datatype]
        return np.dtype(dtype)

    def _to_datatype(self, dtype: np.dtype) -> str:
        as_str = str(dtype)
        datatype = _NumpyToDatatype[as_str]

        return datatype
