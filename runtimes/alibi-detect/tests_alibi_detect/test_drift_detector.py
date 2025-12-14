import numpy as np
import pytest
import mlserver

from typing import List

from alibi_detect.cd import TabularDrift, CVMDriftOnline

from mlserver.types import InferenceRequest, Parameters, RequestInput
from mlserver.codecs import NumpyCodec, NumpyRequestCodec

from mlserver_alibi_detect import AlibiDetectRuntime

from .conftest import P_VAL_THRESHOLD, ERT, WINDOW_SIZES


async def test_load_folder(
    drift_detector: AlibiDetectRuntime,
):
    assert drift_detector.ready
    assert isinstance(drift_detector._model, TabularDrift)


async def test_load_folder_online(
    online_drift_detector: AlibiDetectRuntime,
):
    assert online_drift_detector.ready
    assert isinstance(online_drift_detector._model, CVMDriftOnline)


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

    # Set the return value of the mocked predict method
    mocked_predict.return_value = {"data": {}, "meta": {}}

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


async def test_predict_online(
    online_drift_detector: AlibiDetectRuntime,
    inference_request: InferenceRequest,
):
    # Test a request of length 1
    response = await online_drift_detector.predict(inference_request)
    assert len(response.outputs) == 7
    assert response.outputs[0].name == "is_drift"
    assert response.outputs[0].shape == [1, 1]
    assert response.outputs[1].name == "distance"
    assert response.outputs[2].name == "p_val"
    assert response.outputs[3].name == "threshold"
    assert response.outputs[4].name == "time"
    assert response.outputs[4].data[0] == 1
    assert response.outputs[5].name == "ert"
    assert response.outputs[5].data[0] == ERT
    assert response.outputs[6].name == "test_stat"
    assert response.outputs[6].shape == [1, 1, 3]


async def test_predict_batch_online(online_drift_detector: AlibiDetectRuntime):
    # Send a batch request, the drift detector should run on one instance at a time
    batch_size = 50
    data = np.random.normal(size=(batch_size, 3))
    inference_request = InferenceRequest(
        parameters=Parameters(content_type=NumpyRequestCodec.ContentType),
        inputs=[
            RequestInput(
                name="predict",
                shape=data.shape,
                data=data.tolist(),
                datatype="FP32",
            )
        ],
    )
    response = await online_drift_detector.predict(inference_request)
    assert len(response.outputs) == 7
    assert response.outputs[0].name == "is_drift"
    assert response.outputs[0].shape == [50, 1]
    assert response.outputs[1].name == "distance"
    assert response.outputs[2].name == "p_val"
    assert response.outputs[3].name == "threshold"
    assert response.outputs[4].name == "time"
    assert response.outputs[4].data[-1] == 50
    assert response.outputs[5].name == "ert"
    assert response.outputs[5].data[0] == ERT
    assert response.outputs[6].name == "test_stat"
    assert response.outputs[6].shape == [50, 1, 3]
    # Test stat should be NaN until the test window is filled
    test_stats = NumpyCodec.decode_output(response.outputs[6])
    assert np.isnan(test_stats[0]).all()
    assert not np.isnan(test_stats[WINDOW_SIZES[0]]).all()


async def test_predict_metrics(
    mocker,
    drift_detector: AlibiDetectRuntime,
    inference_request: InferenceRequest,
):
    mlserver_log = mocker.spy(mlserver, "log")

    # For #(batch - 1) requests, outputs should be empty
    batch_size = drift_detector._ad_settings.batch_size
    for _ in range(batch_size - 1):  # type: ignore
        response = await drift_detector.predict(inference_request)
        assert len(response.outputs) == 0

    # By request batch_size, drift should run
    response = await drift_detector.predict(inference_request)

    is_drift = response.outputs[0]
    assert is_drift.shape[1] > 1
    assert mlserver_log.call_count == is_drift.shape[1]
    for call, d in zip(mlserver_log.mock_calls, is_drift.data):
        assert call.kwargs == {"seldon_model_drift": d}


@pytest.mark.parametrize(
    "current_pred, expected",
    [
        ({"data": {"is_drift": [0]}}, [{"seldon_model_drift": 0}]),
        ({"data": {"is_drift": [1]}}, [{"seldon_model_drift": 1}]),
        ({"data": {"is_drift": 0}}, [{"seldon_model_drift": 0}]),
        (
            {"data": {"is_drift": [1, 0, 1]}},
            [
                {"seldon_model_drift": 1},
                {"seldon_model_drift": 0},
                {"seldon_model_drift": 1},
            ],
        ),
        ({"data": {}}, []),
        ({}, []),
    ],
)
def test_log_metrics(
    mocker, current_pred: dict, expected: List[dict], drift_detector: AlibiDetectRuntime
):
    mlserver_log = mocker.spy(mlserver, "log")
    drift_detector._log_metrics(current_pred)

    for call, e in zip(mlserver_log.mock_calls, expected):
        assert call.kwargs == e
