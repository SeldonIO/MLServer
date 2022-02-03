import json

from typing import Any

from starlette.responses import JSONResponse as _JSONResponse

from ..codecs.string import decode_str

try:
    import orjson
except ImportError:
    orjson = None  # type: ignore


class BytesJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            # If we get a bytes payload, try to decode it back to a string on a
            # "best effort" basis
            return decode_str(obj)

        return super().default(self, obj)


class Response(_JSONResponse):
    """
    Custom Response class to use `orjson` if present.
    Otherwise, it'll fall back to the standard JSONResponse.
    """

    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        if orjson is None:
            # Original implementation of starlette's JSONResponse, using our
            # custom encoder (capable of "encoding" bytes).
            # Original implementation can be seen here:
            # https://github.com/encode/starlette/blob/
            # f53faba229e3fa2844bc3753e233d9c1f54cca52/starlette/responses.py#L173-L180
            return json.dumps(
                content,
                ensure_ascii=False,
                allow_nan=False,
                indent=None,
                separators=(",", ":"),
                cls=BytesJSONEncoder,
            ).encode("utf-8")

        # This is equivalent to the ORJSONResponse implementation in FastAPI:
        # https://github.com/tiangolo/fastapi/blob/
        # 864643ef7608d28ac4ed321835a7fb4abe3dfc13/fastapi/responses.py#L32-L34
        return orjson.dumps(content, default=_encode_bytes)


def _encode_bytes(obj: Any) -> str:
    """
    Add compatibility with `bytes` payloads to `orjson`
    """
    if isinstance(obj, bytes):
        # If we get a bytes payload, try to decode it back to a string on a
        # "best effort" basis
        return decode_str(obj)

    raise TypeError
