import hashlib
import asyncio

from typing import Optional

from ..model import MLModel

ENV_HASH_ATTR = "__env_hash__"


def sha256(tarball_path: str) -> str:
    """
    From Python 3.11's implementation of `hashlib.file_digest()`:
    https://github.com/python/cpython/blob/3.11/Lib/hashlib.py#L257
    """
    h = hashlib.sha256()
    buffer_size = 2**18

    # Disable IO buffering since it's handled explicitly below
    with open(tarball_path, "rb", buffering=0) as env_file:
        buffer = bytearray(buffer_size)
        view = memoryview(buffer)
        while True:
            size = env_file.readinto(buffer)
            if size == 0:
                break
            h.update(view[:size])

    return h.hexdigest()


async def get_environment_hash(tarball_path: str) -> str:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, sha256, tarball_path)


def save_environment_hash(model: MLModel, env_hash: str):
    setattr(model, ENV_HASH_ATTR, env_hash)


def read_environment_hash(model: MLModel) -> Optional[str]:
    return getattr(model, ENV_HASH_ATTR, None)
