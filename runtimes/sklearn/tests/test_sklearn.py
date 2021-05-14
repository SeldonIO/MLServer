import pytest
import os

from sklearn.dummy import DummyClassifier
from mlserver.settings import ModelSettings
from mlserver.errors import InferenceError
from mlserver.types import RequestInput, RequestOutput

from mlserver_sklearn import SKLearnModel
from mlserver_sklearn.sklearn import (
    PREDICT_OUTPUT,
    PREDICT_PROBA_OUTPUT,
    WELLKNOWN_MODEL_FILENAMES,
)


def test_load(model: SKLearnModel):
    assert model.ready
    assert type(model._model) == DummyClassifier


@pytest.mark.parametrize("fname", WELLKNOWN_MODEL_FILENAMES)
async def test_load_folder(fname, model_uri: str, model_settings: ModelSettings):
    model_folder = os.path.dirname(model_uri)
    model_path = os.path.join(model_folder, fname)
    os.rename(model_uri, model_path)

    model_settings.parameters.uri = model_path  # type: ignore

    model = SKLearnModel(model_settings)
    await model.load()

    assert model.ready
    assert type(model._model) == DummyClassifier


async def test_multiple_inputs_error(model: SKLearnModel, inference_request):
    inference_request.inputs.append(
        RequestInput(name="input-1", shape=[2], data=[0, 1], datatype="FP32")
    )

    with pytest.raises(InferenceError):
        await model.predict(inference_request)


async def test_invalid_output_error(model: SKLearnModel, inference_request):
    inference_request.outputs = [RequestOutput(name="something_else")]

    with pytest.raises(InferenceError):
        await model.predict(inference_request)


@pytest.mark.parametrize(
    "req_outputs",
    [
        [],
        [PREDICT_OUTPUT],
        [PREDICT_PROBA_OUTPUT],
        [PREDICT_OUTPUT, PREDICT_PROBA_OUTPUT],
    ],
)
async def test_predict(model: SKLearnModel, inference_request, req_outputs):
    inference_request.outputs = [
        RequestOutput(name=req_output) for req_output in req_outputs
    ]

    response = await model.predict(inference_request)

    input_data = inference_request.inputs[0].data
    if len(req_outputs) == 0:
        # Assert that PREDICT_OUTPUT is added by default
        req_outputs = [PREDICT_OUTPUT]

    assert len(response.outputs) == len(req_outputs)
    for req_output, output in zip(req_outputs, response.outputs):
        assert output.name == req_output
        assert output.shape[0] == len(input_data)  # type: ignore
