import asyncio

from typing import Tuple

from aioprocessing import AioJoinableQueue
from mlserver.parallel.worker import WorkerProcess
from mlserver.parallel.messages import ModelUpdateMessage


def test_inference(worker_process: WorkerProcess):
    pass


async def test_load_model(
    model_updates: AioJoinableQueue,
    worker_process: WorkerProcess,
    load_message: ModelUpdateMessage,
):
    loaded_models = await worker_process._model_registry.get_models()
    assert len(list(loaded_models)) == 1

    load_message.model_settings.name = "foo-model"
    await model_updates.coro_put(load_message)
    await model_updates.coro_join()

    loaded_models = list(await worker_process._model_registry.get_models())
    assert len(loaded_models) == 2
    assert loaded_models[1].name == load_message.model_settings.name


async def test_unload_model(
    model_updates: AioJoinableQueue,
    worker_process: WorkerProcess,
    unload_message: ModelUpdateMessage,
):
    loaded_models = await worker_process._model_registry.get_models()
    assert len(list(loaded_models)) == 1

    await model_updates.coro_put(unload_message)
    await model_updates.coro_join()

    loaded_models = list(await worker_process._model_registry.get_models())
    assert len(loaded_models) == 0
