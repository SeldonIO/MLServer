from typing import TYPE_CHECKING

from .numpy import NumpyCodec, NumpyRequestCodec
from .string import StringCodec, StringRequestCodec
from .base64 import Base64Codec
from .datetime import DatetimeCodec
from .errors import CodecError
from .decorator import decode_args
from .base import (
    InputCodec,
    RequestCodec,
    register_input_codec,
    register_request_codec,
    InputCodecLike,
    RequestCodecLike,
)
from .utils import (
    DecodedParameterName,
    has_decoded,
    get_decoded,
    get_decoded_or_raw,
    encode_inference_response,
    encode_response_output,
    decode_request_input,
    decode_inference_request,
)

if TYPE_CHECKING:  # pragma: no cover - type checking only
    from .pandas import PandasCodec as _PandasCodec

__all__ = [
    "CodecError",
    "NumpyCodec",
    "NumpyRequestCodec",
    "StringCodec",
    "StringRequestCodec",
    "Base64Codec",
    "DatetimeCodec",
    "PandasCodec",
    "InputCodec",
    "InputCodecLike",
    "RequestCodec",
    "RequestCodecLike",
    "DecodedParameterName",
    "register_input_codec",
    "register_request_codec",
    "has_decoded",
    "get_decoded",
    "get_decoded_or_raw",
    "encode_inference_response",
    "encode_response_output",
    "decode_request_input",
    "decode_inference_request",
    "decode_args",
]


def __getattr__(name: str):  # pragma: no cover - lightweight lazy import
    if name == "PandasCodec":
        return _load_pandas_codec()

    raise AttributeError(f"module 'mlserver.codecs' has no attribute {name!r}")


def _load_pandas_codec():
    try:
        from .pandas import PandasCodec as _PandasCodec  # Local import to stay optional
    except Exception as exc:  # pragma: no cover - propagate useful context
        raise ImportError(
            "PandasCodec requires the optional 'pandas' dependency"
        ) from exc

    globals()["PandasCodec"] = _PandasCodec
    return _PandasCodec
