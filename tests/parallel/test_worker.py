from multiprocessing import Queue, JoinableQueue
from mlserver.parallel.worker import Worker
from mlserver.parallel.messages import ModelUpdateMessage, InferenceRequestMessage


async def test_predict(
    worker: Worker,
    requests: Queue,
    inference_request_message: InferenceRequestMessage,
    responses: Queue,
):
    requests.put(inference_request_message)
    response = responses.get()

    assert response is not None
    assert response.id == inference_request_message.id

    inference_response = response.inference_response
    assert inference_response.model_name == inference_request_message.model_name
    assert inference_response.model_version == inference_request_message.model_version
    assert len(inference_response.outputs) == 1


async def test_load_model(
    model_updates: JoinableQueue,
    worker: Worker,
    load_message: ModelUpdateMessage,
):
    loaded_models = await worker._model_registry.get_models()
    assert len(list(loaded_models)) == 1

    load_message.model_settings.name = "foo-model"
    model_updates.put(load_message)
    model_updates.join()

    loaded_models = list(await worker._model_registry.get_models())
    assert len(loaded_models) == 2
    assert loaded_models[1].name == load_message.model_settings.name


async def test_unload_model(
    model_updates: JoinableQueue,
    worker: Worker,
    unload_message: ModelUpdateMessage,
):
    loaded_models = await worker._model_registry.get_models()
    assert len(list(loaded_models)) == 1

    model_updates.put(unload_message)
    model_updates.join()

    loaded_models = list(await worker._model_registry.get_models())
    assert len(loaded_models) == 0


async def test_exception(
    worker: Worker,
    requests: Queue,
    inference_request_message: InferenceRequestMessage,
    responses: Queue,
    mocker,
):
    model = await worker._model_registry.get_model(inference_request_message.model_name)
    error_msg = "my foo error"

    async def _async_exception(*args, **kwargs):
        raise Exception(error_msg)

    mocker.patch.object(model, "predict", _async_exception)

    requests.put(inference_request_message)
    response = responses.get()

    assert response is not None
    assert response.id == inference_request_message.id
    assert response.inference_response is None
    assert response.exception is not None
    assert str(response.exception) == error_msg
