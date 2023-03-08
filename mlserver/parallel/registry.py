import asyncio
import os

from typing import Optional, Dict, List

from ..model import MLModel
from ..settings import Settings
from ..env import Environment, compute_hash

from .logging import logger
from .pool import InferencePool, InferencePoolHook

ENV_HASH_ATTR = "__env_hash__"


def _set_environment_hash(model: MLModel, env_hash: str):
    setattr(model, ENV_HASH_ATTR, env_hash)


def _get_environment_hash(model: MLModel) -> Optional[str]:
    return getattr(model, ENV_HASH_ATTR, None)


def _get_env_tarball(model: MLModel) -> Optional[str]:
    if model.settings.parameters is None:
        return None

    return model.settings.parameters.environment_tarball


class InferencePoolRegistry:
    """
    Keeps track of the different inference pools loaded in the server.
    Each inference pool will generally be used to load a different environment.
    """

    def __init__(
        self, settings: Settings, on_worker_stop: List[InferencePoolHook] = []
    ):
        self._settings = settings
        self._on_worker_stop = on_worker_stop
        self._default_pool = InferencePool(
            self._settings, on_worker_stop=on_worker_stop
        )
        self._pools: Dict[str, InferencePool] = {}

        os.makedirs(self._settings.environments_dir, exist_ok=True)

    async def _get_or_create(self, model: MLModel) -> InferencePool:
        env_tarball = _get_env_tarball(model)
        if not env_tarball:
            return self._default_pool

        env_hash = await compute_hash(env_tarball)
        if env_hash in self._pools:
            return self._pools[env_hash]

        env_path = self._get_env_path(env_hash)
        os.makedirs(env_path)
        env = await Environment.from_tarball(env_tarball, env_path, env_hash)
        pool = InferencePool(
            self._settings, env=env, on_worker_stop=self._on_worker_stop
        )
        self._pools[env_hash] = pool
        return pool

    def _get_env_path(self, env_hash: str) -> str:
        return os.path.join(self._settings.environments_dir, env_hash)

    async def _find(self, model: MLModel) -> InferencePool:
        env_hash = _get_environment_hash(model)
        if not env_hash:
            return self._default_pool

        if env_hash not in self._pools:
            # TODO: Raise error for invalid env hash
            pass

        return self._pools[env_hash]

    async def load_model(self, model: MLModel) -> MLModel:
        # TODO: If load fails, should we remove pool if empty?
        pool = await self._get_or_create(model)
        loaded = await pool.load_model(model)
        _set_environment_hash(loaded, pool.env_hash)
        return loaded

    async def reload_model(self, old_model: MLModel, new_model: MLModel) -> MLModel:
        old_hash = _get_environment_hash(old_model)
        new_pool = await self._get_or_create(new_model)

        loaded = await new_pool.reload_model(old_model, new_model)
        _set_environment_hash(loaded, new_pool.env_hash)
        if old_hash != new_pool.env_hash:
            # Environment has changed in the new version, so unload the old one
            await self.unload_model(old_model)

        return loaded

    async def unload_model(self, model: MLModel) -> MLModel:
        pool = await self._find(model)
        unloaded = await pool.unload_model(model)

        if pool != self._default_pool and pool.empty():
            await self._close_pool(pool.env_hash)

        return unloaded

    async def close(self):
        await asyncio.gather(
            self._close_pool(None),
            *[self._close_pool(env_hash) for env_hash in self._pools],
        )

    async def _close_pool(self, env_hash: str = None):
        # TODO: Remove env hash folder
        pool = self._default_pool
        pool_name = "default inference pool"
        if env_hash:
            pool = self._pools[env_hash]
            pool_name = f"inference pool with hash '{env_hash}'"

        logger.info(f"Waiting for shutdown of {pool_name}...")
        await pool.close()
        logger.info(f"Shutdown of {pool_name} complete")

        if env_hash:
            del self._pools[env_hash]
