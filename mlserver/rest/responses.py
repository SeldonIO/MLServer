from typing import Any

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

        # This is equivalent to the ORJSONResponse implementation in FastAPI:
        # https://github.com/tiangolo/fastapi/blob/
        # 864643ef7608d28ac4ed321835a7fb4abe3dfc13/fastapi/responses.py#L32-L34
        return orjson.dumps(content)
