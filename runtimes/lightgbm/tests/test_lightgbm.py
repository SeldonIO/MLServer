import pytest
import os
import lightgbm as lgb

from mlserver.settings import ModelSettings
from mlserver.codecs import CodecError
from mlserver.types import RequestInput, InferenceRequest

from mlserver_lightgbm import LightGBMModel
from mlserver_lightgbm.lightgbm import WELLKNOWN_MODEL_FILENAMES


def test_load(model: LightGBMModel):
    assert model.ready
    assert isinstance(model._model, lgb.Booster)


@pytest.mark.parametrize("fname", WELLKNOWN_MODEL_FILENAMES)
async def test_load_folder(fname, model_uri: str, model_settings: ModelSettings):
    model_folder = os.path.dirname(model_uri)
    model_path = os.path.join(model_folder, fname)
    os.rename(model_uri, model_path)

    model_settings.parameters.uri = model_path  # type: ignore

    model = LightGBMModel(model_settings)
    model.ready = await model.load()

    assert model.ready
    assert isinstance(model._model, lgb.Booster)


async def test_predict(model: LightGBMModel, inference_request: InferenceRequest):
    response = await model.predict(inference_request)

    assert len(response.outputs) == 1
    assert 0 <= response.outputs[0].data[0] <= 1


async def test_multiple_inputs_error(
    model: LightGBMModel, inference_request: InferenceRequest
):
    inference_request.inputs.append(
        RequestInput(name="input-1", shape=[1, 2], data=[[0, 1]], datatype="FP32")
    )

    with pytest.raises(CodecError):
        await model.predict(inference_request)
