import pytest

from mlserver.models.sklearn import _SKLEARN_PRESENT, SKLearnModel
from mlserver.errors import InferenceError

from .helpers import skipif_sklearn_missing

if _SKLEARN_PRESENT:
    from sklearn.dummy import DummyClassifier


@skipif_sklearn_missing
def test_sklearn_load(sklearn_model: SKLearnModel):
    has_loaded = sklearn_model.load()

    assert has_loaded
    assert type(sklearn_model._model) == DummyClassifier


@skipif_sklearn_missing
def test_sklearn_predict_error(sklearn_model: SKLearnModel, inference_request):
    sklearn_model.load()

    with pytest.raises(InferenceError):
        sklearn_model.predict(inference_request)


@skipif_sklearn_missing
def test_sklearn_predict(sklearn_model: SKLearnModel, inference_request):
    sklearn_model.load()

    # Keep only a single input
    inference_request.inputs = inference_request.inputs[:1]
    response = sklearn_model.predict(inference_request)

    assert len(response.outputs[0].data) == len(inference_request.inputs[0].data)
