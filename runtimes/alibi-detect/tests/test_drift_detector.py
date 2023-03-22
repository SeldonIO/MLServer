import numpy as np

from alibi_detect.cd import TabularDrift

from mlserver.types import InferenceRequest
from mlserver.codecs import NumpyRequestCodec

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


async def test_predict_batch(drift_detector: AlibiDetectRuntime, mocker):
    # Mock detector
    mocked_predict = mocker.patch.object(drift_detector._model, "predict")

    # For #(batch - 1) requests, outputs should be empty
    batch_size = drift_detector._ad_settings.batch_size
    expected = np.random.randint(10, size=(batch_size, 3))  # type: ignore
    for idx in range(batch_size - 1):  # type: ignore
        inference_request = NumpyRequestCodec.encode_request(expected[idx : idx + 1])
        response = await drift_detector.predict(inference_request)

        assert len(response.outputs) == 0
        mocked_predict.assert_not_called()

    inference_request = NumpyRequestCodec.encode_request(
        expected[batch_size - 1 : batch_size]  # type: ignore
    )
    await drift_detector.predict(inference_request)

    mocked_predict.assert_called_once()
    payload = mocked_predict.call_args.args[0]
    np.testing.assert_array_equal(payload, expected)


async def test_predict_batch_cleared(
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
    assert len(response.outputs) > 0

    # Batch should now be cleared (and started from scratch)
    response = await drift_detector.predict(inference_request)
    assert len(response.outputs) == 0
