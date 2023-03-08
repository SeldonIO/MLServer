import pytest

from mlserver.model import MLModel
from mlserver.parallel.hash import (
    ENV_HASH_ATTR,
    get_environment_hash,
    save_environment_hash,
    read_environment_hash,
)


@pytest.fixture
async def env_hash(env_tarball: str) -> str:
    return await get_environment_hash(env_tarball)


def test_env_hash(env_hash: str):
    assert len(env_hash) == 64


def test_save(sum_model: MLModel, env_hash: str):
    save_environment_hash(sum_model, env_hash)

    assert hasattr(sum_model, ENV_HASH_ATTR)
    assert getattr(sum_model, ENV_HASH_ATTR) == env_hash


@pytest.mark.parametrize(
    "env_hash",
    ["0e46fce1decb7a89a8b91c71d8b6975630a17224d4f00094e02e1a732f8e95f3", None],
)
def test_save(sum_model: MLModel, env_hash: str):
    if env_hash:
        save_environment_hash(sum_model, env_hash)

    assert read_environment_hash(sum_model) == env_hash
