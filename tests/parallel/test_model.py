import pytest

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
