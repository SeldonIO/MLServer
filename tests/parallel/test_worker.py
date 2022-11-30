from multiprocessing import Queue

from mlserver.settings import ModelSettings
from mlserver.parallel.worker import Worker
from mlserver.parallel.messages import ModelUpdateMessage, ModelRequestMessage




async def test_predict(
    worker: Worker,
    inference_request_message: ModelRequestMessage,
    responses: Queue,
):
    worker.send_request(inference_request_message)
    response = responses.get()

    assert response is not None
    assert response.id == inference_request_message.id

    inference_response = response.return_value
    assert inference_response.model_name == inference_request_message.model_name
    assert inference_response.model_version == inference_request_message.model_version
    assert len(inference_response.outputs) == 1


async def test_metadata(
    worker: Worker,
    metadata_request_message: ModelRequestMessage,
    sum_model_settings: ModelSettings,
    responses: Queue,
):
    worker.send_request(metadata_request_message)
    response = responses.get()

    assert response is not None
    assert response.id == metadata_request_message.id

    metadata_response = response.return_value
    assert metadata_response.name == sum_model_settings.name


async def test_custom_handler(
    worker: Worker,
    custom_request_message: ModelRequestMessage,
    sum_model_settings: ModelSettings,
    responses: Queue,
):
    worker.send_request(custom_request_message)
    response = responses.get()

    assert response is not None
    assert response.id == custom_request_message.id

    custom_response = response.return_value
    assert custom_response == 6


async def test_load_model(
    worker: Worker,
    load_message: ModelUpdateMessage,
    responses: Queue,
):
    loaded_models = await worker._model_registry.get_models()
    assert len(list(loaded_models)) == 1

    new_model_settings = load_message.model_settings.copy()
    new_model_settings.name = "foo-model"
    new_load_message = ModelUpdateMessage(
        update_type=load_message.update_type, model_settings=new_model_settings
    )
    worker.send_update(new_load_message)
    responses.get()

    loaded_models = list(await worker._model_registry.get_models())
    assert len(loaded_models) == 2
    assert loaded_models[0].name == load_message.model_settings.name
    assert loaded_models[1].name == new_load_message.model_settings.name


async def test_unload_model(
    worker: Worker,
    unload_message: ModelUpdateMessage,
    responses: Queue,
):
    loaded_models = await worker._model_registry.get_models()
    assert len(list(loaded_models)) == 1

    worker.send_update(unload_message)
    responses.get()

    loaded_models = list(await worker._model_registry.get_models())
    assert len(loaded_models) == 0


async def test_exception(
    worker: Worker,
    inference_request_message: ModelRequestMessage,
    responses: Queue,
    mocker,
):
    model = await worker._model_registry.get_model(inference_request_message.model_name)
    error_msg = "my foo error"

    async def _async_exception(*args, **kwargs):
        raise Exception(error_msg)

    mocker.patch.object(model, "predict", _async_exception)

    worker.send_request(inference_request_message)
    response = responses.get()

    assert response is not None
    assert response.id == inference_request_message.id
    assert response.return_value is None
    assert response.exception is not None
    assert str(response.exception) == error_msg
