from collections import OrderedDict
from ..cache import ResponseCache


class LocalCache(ResponseCache):
    def __init__(self, size=100):
        self.cache = OrderedDict()
        self.size_limit = size

    async def insert(self, key: str, value: str):
        self.cache[key] = value
        cache_size = await self.size()
        if cache_size > self.size_limit:
            # The cache removes the first entry if it overflows (i.e. in FIFO order)
            self.cache.popitem(last=False)
        return None

    async def lookup(self, key: str) -> str:
        if key in self.cache:
            return self.cache[key]
        else:
            return ""

    async def size(self) -> int:
        return len(self.cache)
