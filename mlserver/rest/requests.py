import orjson

from typing import Any
from fastapi import Request


class ORJSONRequest(Request):
    """
    Custom request class which uses `orjson`.
    """

    async def json(self) -> Any:
        if not hasattr(self, "_json"):
            body = await self.body()
            self._json = orjson.loads(body)
        return self._json
