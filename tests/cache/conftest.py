import pytest

from mlserver.cache.local import LocalCache
from mlserver.cache import ResponseCache

CACHE_SIZE = 10


@pytest.fixture
def local_cache() -> ResponseCache:
    return LocalCache(size=CACHE_SIZE)
