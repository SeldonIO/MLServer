import pytest

from alibi_detect.od import OutlierVAE

from mlserver.settings import ModelSettings
from mlserver.types import RequestInput, InferenceRequest
from mlserver.codecs import CodecError

from mlserver_alibi_detect import AlibiDetectRuntime


async def test_load_folder(outlier_detector: AlibiDetectRuntime):
    assert outlier_detector.ready
    assert type(outlier_detector._model) == OutlierVAE


async def test_predict(
    outlier_detector: AlibiDetectRuntime,
    inference_request: InferenceRequest,
):
    response = await outlier_detector.predict(inference_request)

    assert len(response.outputs) == 3
    assert response.outputs[0].name == "instance_score"
    assert response.outputs[1].name == "feature_score"
    assert response.outputs[2].name == "is_outlier"
    assert response.outputs[2].shape == [1, 1]


async def test_multiple_inputs_error(
    outlier_detector: AlibiDetectRuntime,
    inference_request: InferenceRequest,
):
    inference_request.inputs.append(
        RequestInput(name="input-1", shape=[1, 3], data=[[0, 1, 6]], datatype="FP32")
    )

    with pytest.raises(CodecError):
        await outlier_detector.predict(inference_request)
