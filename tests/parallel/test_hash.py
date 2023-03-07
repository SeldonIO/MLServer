from mlserver.parallel.hash import get_environment_hash


async def test_env_hash(env_tarball: str):
    sha_hash = await get_environment_hash(env_tarball)
    assert len(sha_hash) == 64
