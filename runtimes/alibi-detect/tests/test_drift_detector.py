from alibi_detect.cd import TabularDrift

from mlserver.types import InferenceRequest

from mlserver_alibi_detect import AlibiDetectRuntime

from .conftest import P_VAL_THRESHOLD


async def test_load_folder(
    drift_detector: AlibiDetectRuntime,
):
    assert drift_detector.ready
    assert type(drift_detector._model) == TabularDrift


async def test_predict_batch(
    drift_detector: AlibiDetectRuntime,
    inference_request: InferenceRequest,
):
    # For #(batch - 1) requests, outputs should be empty
    batch_size = drift_detector._ad_settings.batch_size
    for _ in range(batch_size - 1):  # type: ignore
        response = await drift_detector.predict(inference_request)
        assert len(response.outputs) == 0

    # By request batch_size, drift should run
    response = await drift_detector.predict(inference_request)
    assert len(response.outputs) == 4
    assert response.outputs[0].name == "is_drift"
    assert response.outputs[0].shape == [1, 3]
    assert response.outputs[1].name == "distance"
    assert response.outputs[2].name == "p_val"
    assert response.outputs[3].name == "threshold"
    assert response.outputs[3].data[0] == P_VAL_THRESHOLD
