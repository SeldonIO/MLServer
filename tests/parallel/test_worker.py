from aioprocessing import AioJoinableQueue, AioQueue
from mlserver.parallel.worker import Worker
from mlserver.parallel.messages import ModelUpdateMessage, InferenceRequestMessage


async def test_predict(
    worker: Worker,
    requests: AioQueue,
    inference_request_message: InferenceRequestMessage,
    responses: AioQueue,
):
    await requests.coro_put(inference_request_message)
    response = await responses.coro_get()

    assert response is not None
    assert response.id == inference_request_message.id

    inference_response = response.inference_response
    assert inference_response.model_name == inference_request_message.model_name
    assert inference_response.model_version == inference_request_message.model_version
    assert len(inference_response.outputs) == 1


async def test_load_model(
    model_updates: AioJoinableQueue,
    worker: Worker,
    load_message: ModelUpdateMessage,
):
    loaded_models = await worker._model_registry.get_models()
    assert len(list(loaded_models)) == 1

    load_message.model_settings.name = "foo-model"
    await model_updates.coro_put(load_message)
    await model_updates.coro_join()

    loaded_models = list(await worker._model_registry.get_models())
    assert len(loaded_models) == 2
    assert loaded_models[1].name == load_message.model_settings.name


async def test_unload_model(
    model_updates: AioJoinableQueue,
    worker: Worker,
    unload_message: ModelUpdateMessage,
):
    loaded_models = await worker._model_registry.get_models()
    assert len(list(loaded_models)) == 1

    await model_updates.coro_put(unload_message)
    await model_updates.coro_join()

    loaded_models = list(await worker._model_registry.get_models())
    assert len(loaded_models) == 0
