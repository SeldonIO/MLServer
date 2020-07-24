import pytest

from mlserver.models.sklearn import (
    _SKLEARN_PRESENT,
    SKLearnModel,
    PREDICT_OUTPUT,
    PREDICT_PROBA_OUTPUT,
)
from mlserver.errors import InferenceError
from mlserver.types import RequestOutput

from .helpers import skipif_sklearn_missing

if _SKLEARN_PRESENT:
    from sklearn.dummy import DummyClassifier


@skipif_sklearn_missing
def test_sklearn_load(sklearn_model: SKLearnModel):
    assert sklearn_model.ready
    assert type(sklearn_model._model) == DummyClassifier


@skipif_sklearn_missing
def test_sklearn_multiple_inputs_error(sklearn_model: SKLearnModel, inference_request):
    with pytest.raises(InferenceError):
        sklearn_model.predict(inference_request)


@skipif_sklearn_missing
def test_sklearn_invalid_output_error(
    sklearn_model: SKLearnModel, sklearn_inference_request
):
    sklearn_inference_request.outputs.append(RequestOutput(name="something_else"))

    with pytest.raises(InferenceError):
        sklearn_model.predict(sklearn_inference_request)


@skipif_sklearn_missing
@pytest.mark.parametrize(
    "req_outputs",
    [
        [],
        [PREDICT_OUTPUT],
        [PREDICT_PROBA_OUTPUT],
        [PREDICT_OUTPUT, PREDICT_PROBA_OUTPUT],
    ],
)
def test_sklearn_predict(
    sklearn_model: SKLearnModel, sklearn_inference_request, req_outputs
):
    for req_output in req_outputs:
        sklearn_inference_request.outputs.append(RequestOutput(name=req_output))

    response = sklearn_model.predict(sklearn_inference_request)

    input_data = sklearn_inference_request.inputs[0].data
    if len(req_outputs) == 0:
        # Assert that PREDICT_OUTPUT is added by default
        req_outputs = [PREDICT_OUTPUT]

    assert len(response.outputs) == len(req_outputs)
    for req_output, output in zip(req_outputs, response.outputs):
        assert output.name == req_output
        assert len(output.data) == len(input_data)
