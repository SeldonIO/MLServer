import pytest

from alibi_detect.cd import TabularDrift

from mlserver.types import RequestInput, InferenceRequest
from mlserver.codecs import CodecError

from mlserver_alibi_detect import AlibiDetectRuntime

from .conftest import P_VAL_THRESHOLD


async def test_load_folder(
    drift_detector: AlibiDetectRuntime,
):
    assert drift_detector.ready
    assert type(drift_detector._model) == TabularDrift


async def test_predict(
    drift_detector: AlibiDetectRuntime,
    inference_request: InferenceRequest,
):
    response = await drift_detector.predict(inference_request)

    assert len(response.outputs) == 4
    assert response.outputs[0].name == "is_drift"
    assert response.outputs[0].shape == [1, 3]
    assert response.outputs[1].name == "distance"
    assert response.outputs[2].name == "p_val"
    assert response.outputs[3].name == "threshold"
    assert response.outputs[3].data[0] == P_VAL_THRESHOLD


async def test_multiple_inputs_error(
    drift_detector: AlibiDetectRuntime,
    inference_request: InferenceRequest,
):
    inference_request.inputs.append(
        RequestInput(name="input-1", shape=[1, 3], data=[[0, 1, 6]], datatype="FP32")
    )

    with pytest.raises(CodecError):
        await drift_detector.predict(inference_request)
