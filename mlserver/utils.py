import os

from typing import List

from .types import RequestInput
from .settings import ModelSettings
from .errors import InvalidModelURI

try:
    import numpy as np
except ImportError:
    # TODO: Log warning message
    pass

NP_DTYPES = {
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


async def get_model_uri(
    settings: ModelSettings, wellknown_filenames: List[str] = []
) -> str:
    if not settings.parameters:
        raise InvalidModelURI(settings.name)

    model_uri = settings.parameters.uri

    if not model_uri:
        raise InvalidModelURI(settings.name)

    if os.path.isfile(model_uri):
        return model_uri

    if os.path.isdir(model_uri):
        # If model_uri is a folder, search for a well-known model filename
        for fname in wellknown_filenames:
            model_path = os.path.join(model_uri, fname)
            if os.path.isfile(model_path):
                return model_path

        # If none, return the folder
        return model_uri

    # Otherwise, the uri is neither a file nor a folder
    raise InvalidModelURI(settings.name, model_uri)


def to_ndarray(request_input: RequestInput) -> "np.ndarray":
    dtype = to_dtype(request_input.datatype)
    data = getattr(request_input.data, "__root__", request_input.data)

    model_data = np.array(data, dtype=dtype)

    # TODO: Check if reshape not valid
    return model_data.reshape(request_input.shape)


def to_dtype(datatype: str) -> "np.dtype":
    # TODO: Validate datatype earlier (in Pydantic)
    dtype = NP_DTYPES[datatype]
    return np.dtype(dtype)
