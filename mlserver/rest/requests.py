from typing import Any
from gzip import decompress as gzip_decompress
from fastapi import Request as _Request

try:
    import orjson
except ImportError:
    orjson = None  # type: ignore


class Request(_Request):
    """
    Custom request class which uses `orjson` if present.
    Otherwise, it falls back to the standard FastAPI request.
    """

    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "gzip" in self.headers.getlist("Content-Encoding"):
                body = gzip_decompress(body)
            self._body = body
        return self._body

    async def json(self) -> Any:
        if orjson is None:
            return await super().json()

        if not hasattr(self, "_json"):
            body = await self.body()
            self._json = orjson.loads(body)

        return self._json
