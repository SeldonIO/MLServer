import pytest
import os

from mlserver.models.sklearn import _SKLEARN_PRESENT, SKLearnModel
from mlserver.settings import ModelSettings, ModelParameters
from mlserver.types import InferenceRequest

if _SKLEARN_PRESENT:
    import joblib
    import numpy as np

    from sklearn.dummy import DummyClassifier


@pytest.fixture
def sklearn_model_uri(tmp_path) -> str:
    n = 4
    X = np.random.rand(n)
    y = np.random.rand(n)

    clf = DummyClassifier()
    clf.fit(X, y)

    model_uri = os.path.join(tmp_path, "model.joblib")
    joblib.dump(clf, model_uri)

    return model_uri


@pytest.fixture
def sklearn_model(sklearn_model_uri: str) -> SKLearnModel:
    model_settings = ModelSettings(
        name="sklearn-model",
        version="v1.2.3",
        parameters=ModelParameters(uri=sklearn_model_uri),
    )
    model = SKLearnModel(model_settings)
    model.load()

    return model


@pytest.fixture
def sklearn_inference_request(inference_request: InferenceRequest) -> InferenceRequest:
    # Keep only a single input
    inference_request.inputs = inference_request.inputs[:1]

    return inference_request
