from string import ascii_lowercase

from .conftest import CACHE_SIZE


async def test_local_cache_lookup(local_cache):
    assert await local_cache.size() == 0
    assert await local_cache.lookup("unknown key") == ""
    assert await local_cache.size() == 0


async def test_local_cache_insert(local_cache):
    assert await local_cache.size() == 0

    await local_cache.insert("key", "value")
    assert await local_cache.lookup("key") == "value"

    assert await local_cache.size() == 1

    await local_cache.insert("new key", "new value")
    assert await local_cache.lookup("key") == "value"
    assert await local_cache.lookup("new key") == "new value"

    assert await local_cache.size() == 2


async def test_local_cache_rotate(local_cache):
    # Insert alphabets on a loop
    for key, symbol in enumerate(ascii_lowercase):
        await local_cache.insert(str(key), symbol)

        if key < CACHE_SIZE:
            assert await local_cache.size() == key + 1
            assert await local_cache.lookup(str(key)) == symbol

        else:
            assert await local_cache.size() == CACHE_SIZE
            assert await local_cache.lookup(str(key)) == symbol
            assert await local_cache.lookup(str(key - CACHE_SIZE)) == ""
