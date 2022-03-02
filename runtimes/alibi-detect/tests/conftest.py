import pytest
import os
import numpy as np

from mlserver.settings import ModelSettings, ModelParameters
from mlserver.types import InferenceRequest
from mlserver_alibi_detect import AlibiDetectRuntime

from alibi_detect.utils.saving import save_detector
from alibi_detect.cd import TabularDrift

TESTS_PATH = os.path.dirname(__file__)
TESTDATA_PATH = os.path.join(TESTS_PATH, "testdata")


def pytest_collection_modifyitems(items):
    """
    Add pytest.mark.asyncio marker to every test.
    """
    for item in items:
        item.add_marker("asyncio")


@pytest.fixture
def model_uri(tmp_path) -> str:
    X_ref = np.array([[1, 2, 3]])

    cd = TabularDrift(X_ref, p_val=0.05)

    detector_uri = os.path.join(tmp_path, "alibi-detector-artifacts")
    save_detector(cd, detector_uri)

    return detector_uri


@pytest.fixture
def model_settings(model_uri: str) -> ModelSettings:
    return ModelSettings(
        name="alibi-detect-model",
        parameters=ModelParameters(
            uri=model_uri,
            version="v1.2.3",
            extra={"predict_parameters": {"drift_type": "feature"}},
        ),
    )


@pytest.fixture
async def model(model_settings: ModelSettings) -> AlibiDetectRuntime:
    model = AlibiDetectRuntime(model_settings)
    await model.load()

    return model


@pytest.fixture
def inference_request() -> InferenceRequest:
    payload_path = os.path.join(TESTDATA_PATH, "inference-request.json")
    return InferenceRequest.parse_file(payload_path)
