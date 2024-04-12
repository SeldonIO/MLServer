import pytest
import os
from catboost import CatBoostClassifier

from mlserver.settings import ModelSettings
from mlserver.codecs import CodecError
from mlserver.types import RequestInput, InferenceRequest

from mlserver_catboost import CatboostModel
from mlserver_catboost.catboost import WELLKNOWN_MODEL_FILENAMES


def test_load(model: CatboostModel):
    assert model.ready
    assert isinstance(model._model, CatBoostClassifier)


@pytest.mark.parametrize("fname", WELLKNOWN_MODEL_FILENAMES)
async def test_load_folder(fname, model_uri: str, model_settings: ModelSettings):
    model_folder = os.path.dirname(model_uri)
    model_path = os.path.join(model_folder, fname)
    os.rename(model_uri, model_path)

    model_settings.parameters.uri = model_path  # type: ignore

    model = CatboostModel(model_settings)
    await model.load()

    assert model.ready
    assert isinstance(model._model, CatBoostClassifier)


async def test_predict(model: CatboostModel, inference_request: InferenceRequest):
    response = await model.predict(inference_request)

    assert len(response.outputs) == 1
    assert 0 <= response.outputs[0].data[0] <= 1


async def test_multiple_inputs_error(
    model: CatboostModel, inference_request: InferenceRequest
):
    inference_request.inputs.append(
        RequestInput(name="input-1", shape=[1, 2], data=[[0, 1]], datatype="FP32")
    )

    with pytest.raises(CodecError):
        await model.predict(inference_request)
