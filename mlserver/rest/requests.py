from typing import Any

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

    async def json(self) -> Any:
        if orjson is None:
            return await super().json()

        if not hasattr(self, "_json"):
            body = await self.body()
            self._json = orjson.loads(body)

        return self._json
