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
