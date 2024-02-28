import os

import pandas as pd
import pytest
from mlserver_sklearn import SKLearnModel
from mlserver_sklearn.sklearn import (
    PREDICT_OUTPUT,
    PREDICT_PROBA_OUTPUT,
    WELLKNOWN_MODEL_FILENAMES,
    PREDICT_TRANSFORM,
)
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.pipeline import Pipeline

from mlserver.codecs import CodecError
from mlserver.errors import InferenceError
from mlserver.settings import ModelSettings
from mlserver.types import RequestInput, RequestOutput, Parameters


def test_load(model: SKLearnModel):
    assert model.ready
    assert isinstance(model._model, DummyClassifier)


def test_regression_load(regression_model: SKLearnModel):
    assert regression_model.ready
    assert isinstance(regression_model._model, DummyRegressor)


def test_pandas_load(pandas_model: SKLearnModel):
    assert pandas_model.ready
    assert isinstance(pandas_model._model, Pipeline)


@pytest.mark.parametrize("fname", WELLKNOWN_MODEL_FILENAMES)
async def test_load_folder(fname, model_uri: str, model_settings: ModelSettings):
    model_folder = os.path.dirname(model_uri)
    model_path = os.path.join(model_folder, fname)
    os.rename(model_uri, model_path)

    model_settings.parameters.uri = model_path  # type: ignore

    model = SKLearnModel(model_settings)
    model.ready = await model.load()

    assert model.ready
    assert isinstance(model._model, DummyClassifier)


async def test_multiple_inputs_error(model: SKLearnModel, inference_request):
    inference_request.inputs.append(
        RequestInput(name="input-1", shape=[2], data=[0, 1], datatype="FP32")
    )

    with pytest.raises(CodecError):
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


@pytest.mark.parametrize(
    "req_outputs",
    [[], [PREDICT_OUTPUT]],
)
async def test_pandas_predict(
    pandas_model: SKLearnModel, pandas_inference_request, req_outputs
):
    # The `pandas_model` is a regression model that does not support `predict_proba`
    pandas_inference_request.outputs = [
        RequestOutput(name=req_output) for req_output in req_outputs
    ]

    response = await pandas_model.predict(pandas_inference_request)

    input_data = pandas_inference_request.inputs[0].data
    if len(req_outputs) == 0:
        # Assert that PREDICT_OUTPUT is added by default
        req_outputs = [PREDICT_OUTPUT]

    assert len(response.outputs) == len(req_outputs)
    for req_output, output in zip(req_outputs, response.outputs):
        assert output.name == req_output
        assert output.shape[0] == len(input_data)  # type: ignore


async def test_no_predict_proba_for_regression_models(
    regression_model: SKLearnModel, inference_request
):
    inference_request.outputs = [RequestOutput(name=PREDICT_PROBA_OUTPUT)]

    with pytest.raises(InferenceError):
        await regression_model.predict(inference_request)


async def test_no_predict_proba_for_regression_pipelines(
    pandas_model: SKLearnModel, pandas_inference_request
):
    pandas_inference_request.outputs = [RequestOutput(name=PREDICT_PROBA_OUTPUT)]

    with pytest.raises(InferenceError):
        await pandas_model.predict(pandas_inference_request)


async def test_error_on_multiple_dataframe_outputs(
    dataframe_model: SKLearnModel, inference_request
):
    inference_request.outputs = [
        RequestOutput(name=PREDICT_OUTPUT, parameters=Parameters(content_type="pd")),
        RequestOutput(
            name=PREDICT_PROBA_OUTPUT, parameters=Parameters(content_type="pd")
        ),
    ]
    with pytest.raises(InferenceError) as e:
        await dataframe_model.predict(inference_request)

    assert "Cannot encode" in str(e.value)


async def test_dataframe_model_output(dataframe_model: SKLearnModel, inference_request):
    inference_request.outputs = [
        RequestOutput(name=PREDICT_OUTPUT, parameters=Parameters(content_type="pd"))
    ]
    # Test that one `predict` output that returns columnar data in a pd.DataFrame can
    # be encoded as multiple named outputs
    response = await dataframe_model.predict(inference_request)

    raw_response: pd.DataFrame = dataframe_model._model.predict("")
    expected_output_names = list(raw_response.columns)

    assert len(response.outputs) == len(expected_output_names)

    output_names = [o.name for o in response.outputs]
    assert str(output_names) == str(expected_output_names)


@pytest.mark.parametrize(
    "req_outputs",
    [[], [PREDICT_TRANSFORM]],
)
async def test_preprocessor(
    pandas_preprocessor: SKLearnModel, pandas_inference_request, req_outputs
):
    # The `pandas_model` is a regression model that does not support `predict_proba`
    pandas_inference_request.outputs = [
        RequestOutput(name=req_output) for req_output in req_outputs
    ]

    response = await pandas_preprocessor.predict(pandas_inference_request)

    input_data = pandas_inference_request.inputs[0].data
    if len(req_outputs) == 0:
        # Assert that PREDICT_OUTPUT is added by default
        req_outputs = [PREDICT_TRANSFORM]

    assert len(response.outputs) == len(req_outputs)
    for req_output, output in zip(req_outputs, response.outputs):
        assert output.name == req_output
        assert output.shape[0] == len(input_data)  # type: ignore
