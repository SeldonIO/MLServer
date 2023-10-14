from ..cache import ResponseCache


class LocalCache(ResponseCache):
    def __init__(self):
        self.cache = {}

    async def insert(self, key: str, value: str):
        self.cache[key] = value
        return None

    async def lookup(self, key: str) -> str:
        if key in self.cache:
            return self.cache[key]
        else:
            return None
