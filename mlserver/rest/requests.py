from typing import Any

from fastapi import Request as _Request

try:
    import orjson
except ImportError:
    orjson = None


class _ORJSONRequest(_Request):
    """
    Custom request class which uses `orjson`.
    """

    async def json(self) -> Any:
        if not hasattr(self, "_json"):
            body = await self.body()
            self._json = orjson.loads(body)
        return self._json


Request = _Request if orjson is None else _ORJSONRequest
