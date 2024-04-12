import pytest
import os
import xgboost as xgb

from typing import List

from mlserver.errors import InferenceError
from mlserver.settings import ModelSettings
from mlserver.codecs import CodecError
from mlserver.types import RequestOutput, RequestInput, InferenceRequest

from mlserver_xgboost import XGBoostModel
from mlserver_xgboost.xgboost import (
    PREDICT_OUTPUT,
    PREDICT_PROBA_OUTPUT,
)


def test_load(model: XGBoostModel):
    assert model.ready
    assert isinstance(model._model, xgb.XGBRegressor)


def test_load_classifier(classifier: XGBoostModel):
    assert classifier.ready
    assert isinstance(classifier._model, xgb.XGBClassifier)


async def test_load_folder(model_uri: str, model_settings: ModelSettings):
    # Rename `xgboost-model.[ext]` to `model.[ext]`
    _, ext = os.path.splitext(model_uri)
    fname = f"model{ext}"
    model_folder = os.path.dirname(model_uri)
    model_path = os.path.join(model_folder, fname)
    os.rename(model_uri, model_path)

    model_settings.parameters.uri = model_folder  # type: ignore

    model = XGBoostModel(model_settings)
    model.ready = await model.load()

    assert model.ready
    assert isinstance(model._model, xgb.XGBRegressor)


async def test_predict(model: XGBoostModel, inference_request: InferenceRequest):
    response = await model.predict(inference_request)

    assert len(response.outputs) == 1
    assert 0 <= response.outputs[0].data[0] <= 1


@pytest.mark.parametrize(
    "req_outputs",
    [
        [],
        [PREDICT_OUTPUT],
        [PREDICT_PROBA_OUTPUT],
        [PREDICT_OUTPUT, PREDICT_PROBA_OUTPUT],
    ],
)
async def test_predict_classifier(
    classifier: XGBoostModel,
    inference_request: InferenceRequest,
    req_outputs: List[str],
):
    inference_request.outputs = [
        RequestOutput(name=req_output) for req_output in req_outputs
    ]
    response = await classifier.predict(inference_request)

    input_data = inference_request.inputs[0].data
    if len(req_outputs) == 0:
        # Assert that PREDICT_OUTPUT is added by default
        req_outputs = [PREDICT_OUTPUT]

    assert len(response.outputs) == len(req_outputs)
    for req_output, output in zip(req_outputs, response.outputs):
        assert output.name == req_output
        assert output.shape[0] == len(input_data)  # type: ignore


@pytest.mark.parametrize("invalid_output", ["something_else", PREDICT_PROBA_OUTPUT])
async def test_invalid_output_error(
    model: XGBoostModel, inference_request: InferenceRequest, invalid_output: str
):
    inference_request.outputs = [RequestOutput(name=invalid_output)]

    with pytest.raises(InferenceError):
        await model.predict(inference_request)


async def test_multiple_inputs_error(
    model: XGBoostModel, inference_request: InferenceRequest
):
    inference_request.inputs.append(
        RequestInput(name="input-1", shape=[1, 2], data=[[0, 1]], datatype="FP32")
    )

    with pytest.raises(CodecError):
        await model.predict(inference_request)
