import pytest
from mlserver.settings import ModelSettings, ModelParameters
from mlserver.types import RequestInput, InferenceRequest
from mlserver.codecs import CodecError
from mlserver_alibi_detect import AlibiDetectRuntime
from alibi_detect.cd import TabularDrift
from alibi_detect.utils.saving import save_detector
import os
import numpy as np

P_VAL_THRESHOLD = 0.05


@pytest.fixture
def alibi_detect_tabular_drift_model_settings(
    alibi_detect_tabular_drift_model_uri: str,
) -> ModelSettings:
    return ModelSettings(
        name="alibi-detect-model",
        parameters=ModelParameters(
            uri=alibi_detect_tabular_drift_model_uri,
            version="v1.2.3",
            extra={"predict_parameters": {"drift_type": "feature"}},
        ),
    )


@pytest.fixture
def alibi_detect_tabular_drift_model_uri(tmp_path) -> str:
    X_ref = np.array([[1, 2, 3]])

    cd = TabularDrift(X_ref, p_val=P_VAL_THRESHOLD)

    detector_uri = os.path.join(tmp_path, "alibi-detector-artifacts")
    save_detector(cd, detector_uri)

    return detector_uri


@pytest.fixture
async def alibi_detect_tabular_drift_model(
    alibi_detect_tabular_drift_model_settings: ModelSettings,
) -> AlibiDetectRuntime:
    model = AlibiDetectRuntime(alibi_detect_tabular_drift_model_settings)
    await model.load()

    return model


async def test_load_folder(
    alibi_detect_tabular_drift_model_uri: str,
    alibi_detect_tabular_drift_model_settings: ModelSettings,
):

    alibi_detect_tabular_drift_model_settings.parameters.uri = (  # type: ignore
        alibi_detect_tabular_drift_model_uri
    )

    model = AlibiDetectRuntime(alibi_detect_tabular_drift_model_settings)
    await model.load()

    assert model.ready
    assert type(model._model) == TabularDrift


async def test_predict(
    alibi_detect_tabular_drift_model: AlibiDetectRuntime,
    inference_request: InferenceRequest,
):
    response = await alibi_detect_tabular_drift_model.predict(inference_request)

    assert len(response.outputs) == 4
    assert response.outputs[0].name == "is_drift"
    assert response.outputs[0].shape == [1, 3]
    assert response.outputs[1].name == "distance"
    assert response.outputs[2].name == "p_val"
    assert response.outputs[3].name == "threshold"
    assert response.outputs[3].data[0] == P_VAL_THRESHOLD


async def test_multiple_inputs_error(
    alibi_detect_tabular_drift_model: AlibiDetectRuntime,
    inference_request: InferenceRequest,
):
    inference_request.inputs.append(
        RequestInput(name="input-1", shape=[1, 3], data=[[0, 1, 6]], datatype="FP32")
    )

    with pytest.raises(CodecError):
        await alibi_detect_tabular_drift_model.predict(inference_request)
