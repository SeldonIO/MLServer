import os
import pytest

from mlserver.codecs import CodecError
from mlserver.types import RequestInput, InferenceRequest

from mlserver_alibi_detect import AlibiDetectRuntime


async def test_multiple_inputs_error(
    outlier_detector: AlibiDetectRuntime,
    inference_request: InferenceRequest,
):
    inference_request.inputs.append(
        RequestInput(name="input-1", shape=[1, 3], data=[[0, 1, 6]], datatype="FP32")
    )

    with pytest.raises(CodecError):
        await outlier_detector.predict(inference_request)


async def test_saving_state(
    online_drift_detector: AlibiDetectRuntime,
    inference_request: InferenceRequest,
):
    save_freq = online_drift_detector._ad_settings.state_save_freq
    state_uri = os.path.join(online_drift_detector._model_uri, "state")

    # Check nothing written after (save_freq -1) requests
    for _ in range(save_freq - 1):  # type: ignore
        await online_drift_detector.predict(inference_request)
    assert not os.path.isdir(state_uri)

    # Check state written after (save_freq) requests
    await online_drift_detector.predict(inference_request)
    assert os.path.isdir(state_uri)

    # Check state properly loaded in new runtime
    new_online_drift_detector = AlibiDetectRuntime(online_drift_detector.settings)
    await new_online_drift_detector.load()
    assert new_online_drift_detector._model.t == save_freq
