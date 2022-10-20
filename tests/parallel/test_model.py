import pytest

from mlserver.handlers.custom import get_custom_handlers
from mlserver.types import InferenceRequest, MetadataModelResponse
from mlserver.model import MLModel
from mlserver.settings import ModelSettings

from ..fixtures import ErrorModel


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
    with pytest.raises(Exception) as excinfo:
        await error_model.predict(inference_request)

    assert str(excinfo.value) == ErrorModel.error_message


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
