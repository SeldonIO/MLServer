import pytest

from mlserver.errors import MLServerError
from mlserver.handlers.custom import get_custom_handlers
from mlserver.types import InferenceRequest, MetadataModelResponse
from mlserver.model import MLModel
from mlserver.settings import ModelSettings
from mlserver.parallel.pool import InferencePool

from ..fixtures import ErrorModel


@pytest.fixture
async def sum_model(inference_pool: InferencePool, sum_model: MLModel) -> MLModel:
    parallel_model = await inference_pool.load_model(sum_model)

    yield parallel_model

    await inference_pool.unload_model(sum_model)


async def test_predict(
    sum_model: MLModel,
    sum_model_settings: ModelSettings,
    inference_request: InferenceRequest,
):
    inference_response = await sum_model.predict(inference_request)

    assert inference_response.id == inference_request.id
    assert inference_response.model_name == sum_model_settings.name
    assert len(inference_response.outputs) == 1


async def test_predict_error(
    error_model: MLModel,
    inference_request: InferenceRequest,
):
    with pytest.raises(MLServerError) as excinfo:
        await error_model.predict(inference_request)

    expected_msg = f"mlserver.errors.MLServerError: {ErrorModel.error_message}"
    assert str(excinfo.value) == expected_msg


async def test_metadata(
    sum_model: MLModel,
    sum_model_settings: ModelSettings,
):
    metadata = await sum_model.metadata()

    assert isinstance(metadata, MetadataModelResponse)
    assert metadata.name == sum_model_settings.name


async def test_metadata_cached(
    sum_model: MLModel, sum_model_settings: ModelSettings, mocker
):
    expected_metadata = MetadataModelResponse(name="foo", platform="bar")

    async def _send(*args, **kwargs) -> MetadataModelResponse:
        return expected_metadata

    send_stub = mocker.stub("_send")
    send_stub.side_effect = _send
    sum_model._send = send_stub

    metadata_1 = await sum_model.metadata()
    metadata_2 = await sum_model.metadata()

    assert metadata_1 == expected_metadata
    assert metadata_2 == expected_metadata
    send_stub.assert_called_once()


async def test_custom_handlers(sum_model: MLModel):
    handlers = get_custom_handlers(sum_model)
    assert len(handlers) == 2

    response = await sum_model.my_payload([1, 2, 3])
    assert response == 6
