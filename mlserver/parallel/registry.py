from typing import Dict, List

from ..settings import Settings
from ..pool import InferencePool, InferencePoolHook
from .hash import get_environment_hash, save_environment_hash, read_environment_hash


def _get_environment_path(model: MLModel) -> Optional[str]:
    if model.settings.parameters is None:
        return None

    return model.settings.parameters.environment_path


class InferencePoolRegistry:
    """
    Keeps track of the different inference pools loaded in the server.
    Each inference pool will generally be used to load a different environment.
    """

    def __init__(
        self, settings: Settings, on_worker_stop: List[InferencePoolHook] = []
    ):
        self._on_worker_stop = on_worker_stop
        self._default_pool = InferencePool(settings, on_worker_stop=on_worker_stop)
        self._pools: Dict[str, InferencePool] = {}

    async def _get_or_create(self, model: MLModel) -> InferencePool:
        env_path = _get_environment_path(model)
        if not env_path:
            return self._default_pool

        env_hash = await get_environment_hash(env_path)
        save_environment_hash(model, env_hash)
        if env_hash in self._pools:
            return self._pools[env_hash]

        env = await Environment.from_tarball(env_path)
        pool = InferencePool(settings, env=env, on_worker_stop=self._on_worker_stop)
        self._pools[env_hash] = pool
        return pool

    async def _find(self, model: MLModel) -> InferencePool:
        env_hash = read_environment_hash(model)
        if not env_hash:
            return self._default_pool

        if env_hash not in self._pools:
            # TODO: Raise error for invalid env hash
            pass

        return self._pools[env_hash]

    async def load_model(self, model: MLModel) -> MLModel:
        pool = await self._get_or_create(model)
        return await pool.load_model(model)

    async def reload_model(self, old_model: MLModel, new_model: MLModel) -> MLModel:
        # TODO: What if env is now different?
        old_pool = self._find(old_model)
        new_pool = self._get_or_create(new_model)

        loaded = await new_pool.load_model(new_model)
        if old_pool != new_model:
            # Unload from old one
            await pool.unload_model

        return loaded

    async def unload_model(self, model: MLModel) -> MLModel:
        pool = self._find(model)
        unloaded = await pool.unload_model(model)

        if pool != self._default_pool:
            # TODO: If pool is now empty, remove it
            pass

        return unloaded

    async def close(self):
        await asyncio.gather(
            self._close_pool(None),
            *[self._close_pool(env_hash) for env_hash in self._pools],
        )

    async def _close_pool(env_hash: str = None):
        pool = self._default_pool
        pool_name = "default inference pool"
        if env_hash is None:
            pool = self._pools[env_hash]
            pool_name = f"inference pool with hash '{env_hash}'"

        logger.info(f"Waiting for shutdown of {pool_name}...")
        await pool.close()
        logger.info(f"Shutdown of {pool_name} complete")
