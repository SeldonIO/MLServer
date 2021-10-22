from typing import Any, Type

from fastapi.responses import ORJSONResponse as _ORJSONResponse
from starlette.responses import JSONResponse as _JSONResponse

try:
    import orjson
except ImportError:
    orjson = None  # type: ignore


class Response(_JSONResponse):
    """
    Custom Response class to use `orjson` if present.
    Otherwise, it'll fall back to the standard JSONResponse.
    """

    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        if orjson is None:
            return super().render(content)

        return orjson.dumps(content)
