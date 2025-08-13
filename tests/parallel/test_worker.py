import pytest
from multiprocessing import Queue

from mlserver.settings import ModelSettings
from mlserver.codecs import StringCodec
from mlserver.parallel.errors import WorkerError
from mlserver.parallel.worker import Worker
from mlserver.parallel.messages import (
    ModelUpdateMessage,
    ModelRequestMessage,
    # NEW for streaming assertions:
    ModelStreamChunkMessage,
    ModelStreamEndMessage,
    ModelResponseMessage,
)
from mlserver.types import InferenceRequest
from mlserver.parallel.model import ModelMethods


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
    assert response.exception.__class__ == WorkerError
    assert str(response.exception) == f"builtins.Exception: {error_msg}"


# ---------------------------
# NEW: streaming-specific tests
# ---------------------------


async def test_streaming_success(
    worker: Worker,
    stream_request_message: ModelRequestMessage,
    responses: Queue,
    mocker,
):
    """
    Verify that the worker emits chunk messages and an end message for an
    async-generator model method, plus the final unary ack.
    """
    model = await worker._model_registry.get_model(stream_request_message.model_name)

    async def stream_tokens(*args, **kwargs):
        async def agen():
            yield b"tok1"
            yield b"tok2"

        return agen()

    # Important: create=True lets us add a new attribute that isn't present
    mocker.patch.object(model, "stream_tokens", stream_tokens, create=True)

    # Drive the worker
    worker.send_request(stream_request_message)

    # Expect: chunk, chunk, end, then unary ack ModelResponseMessage
    msg1 = responses.get()
    msg2 = responses.get()
    msg3 = responses.get()
    msg4 = responses.get()

    assert isinstance(msg1, ModelStreamChunkMessage)
    assert msg1.id == stream_request_message.id and msg1.chunk == b"tok1"

    assert isinstance(msg2, ModelStreamChunkMessage)
    assert msg2.id == stream_request_message.id and msg2.chunk == b"tok2"

    assert isinstance(msg3, ModelStreamEndMessage)
    assert msg3.id == stream_request_message.id and msg3.exception is None

    assert isinstance(msg4, ModelResponseMessage)
    assert msg4.id == stream_request_message.id and msg4.return_value is None


async def test_streaming_error(
    worker: Worker,
    stream_error_request_message: ModelRequestMessage,
    responses: Queue,
    mocker,
):
    """
    Verify that a mid-stream error results in an END message carrying an
    exception, plus the unary ack.
    """
    model = await worker._model_registry.get_model(
        stream_error_request_message.model_name
    )

    async def stream_tokens_err(*args, **kwargs):
        async def agen():
            yield b"ok"
            # Use a picklable (built-in) exception type for multiprocessing.Queue
            raise RuntimeError("kaboom")

        return agen()

    # Important: create=True since the attribute doesn't exist on SumModel
    mocker.patch.object(model, "stream_tokens_err", stream_tokens_err, create=True)

    worker.send_request(stream_error_request_message)

    # Expect: one chunk, then END with exception, then unary ack
    msg1 = responses.get()
    msg2 = responses.get()
    msg3 = responses.get()

    assert isinstance(msg1, ModelStreamChunkMessage)
    assert msg1.id == stream_error_request_message.id and msg1.chunk == b"ok"

    assert isinstance(msg2, ModelStreamEndMessage)
    assert msg2.id == stream_error_request_message.id and msg2.exception is not None
    assert "kaboom" in str(msg2.exception)

    assert isinstance(msg3, ModelResponseMessage)
    assert msg3.id == stream_error_request_message.id and msg3.return_value is None


# ---------------------------
# MODIFIED: for speed
# ---------------------------


async def test_worker_env(
    worker_with_env: Worker,
    responses: Queue,
    env_model_settings: ModelSettings,
    inference_request: InferenceRequest,
):
    # Build a fresh request targeting the env model
    env_req = ModelRequestMessage(
        model_name=env_model_settings.name,
        model_version=env_model_settings.version,
        method_name=ModelMethods.Predict.value,
        method_args=[inference_request],
        method_kwargs={},
    )

    worker_with_env.send_request(env_req)

    # Avoid indefinite hang: fail fast if nothing arrives
    try:
        response_message = responses.get(timeout=5)
    except Exception as e:
        pytest.fail(f"No response received from env worker within timeout: {e}")

    assert response_message is not None
    assert response_message.id == env_req.id
    assert response_message.exception is None

    response = response_message.return_value
    assert response is not None
    assert len(response.outputs) == 1

    # Note: These versions come from the `environment.yml` found in
    # `./tests/testdata/environment.yaml`
    assert response.outputs[0].name == "sklearn_version"
    [sklearn_version] = StringCodec.decode_output(response.outputs[0])
    assert sklearn_version == "1.3.1"
