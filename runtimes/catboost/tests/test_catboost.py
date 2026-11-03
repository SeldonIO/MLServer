import pytest
import os
from catboost import CatBoostClassifier

from mlserver.settings import ModelSettings
from mlserver.codecs import CodecError, NumpyRequestCodec
from mlserver.types import RequestInput, RequestOutput, InferenceRequest
from mlserver.errors import InferenceError
import numpy as np

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


async def test_predict_proba_env(model, inference_request, monkeypatch):
    monkeypatch.setenv("PREDICT_PROBA", "true")
    inference_request.outputs = None
    response = await model.predict(inference_request)
    decoded = model.decode_request(inference_request, default_codec=NumpyRequestCodec)
    actual = np.asarray(response.outputs[0].data).reshape(response.outputs[0].shape)
    np.testing.assert_allclose(
        actual, np.atleast_2d(model._model.predict_proba(decoded))
    )
    assert response.outputs[0].name == "predict_proba"
    assert actual.shape == (1, 2)


async def test_predict_default_unchanged(model, inference_request, monkeypatch):
    monkeypatch.delenv("PREDICT_PROBA", raising=False)
    inference_request.outputs = None
    response = await model.predict(inference_request)
    assert response.outputs[0].name == "predict"
    decoded = model.decode_request(inference_request, default_codec=NumpyRequestCodec)
    actual = np.asarray(response.outputs[0].data).reshape(response.outputs[0].shape)
    np.testing.assert_array_equal(
        actual.squeeze(), model._model.predict(decoded).squeeze()
    )


async def test_requested_outputs_override_env(model, inference_request, monkeypatch):
    monkeypatch.setenv("PREDICT_PROBA", "true")
    inference_request.outputs = [
        RequestOutput(name="predict"),
        RequestOutput(name="predict_proba"),
    ]
    response = await model.predict(inference_request)
    assert [out.name for out in response.outputs] == ["predict", "predict_proba"]
    decoded = model.decode_request(inference_request, default_codec=NumpyRequestCodec)
    proba = np.asarray(response.outputs[1].data).reshape(response.outputs[1].shape)
    np.testing.assert_allclose(
        proba, np.atleast_2d(model._model.predict_proba(decoded))
    )


async def test_model_setting_overrides_env(model, inference_request, monkeypatch):
    monkeypatch.setenv("PREDICT_PROBA", "true")
    model.settings.parameters.extra = {"predict_fn": "predict"}
    inference_request.outputs = None
    response = await model.predict(inference_request)
    assert response.outputs[0].name == "predict"


async def test_invalid_output(model, inference_request):
    inference_request.outputs = [RequestOutput(name="invalid")]
    with pytest.raises(InferenceError):
        await model.predict(inference_request)
