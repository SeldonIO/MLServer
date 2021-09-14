import numpy as np

from mlserver.codecs import NumpyCodec
from mlserver.types import InferenceRequest, Parameters, RequestInput
from mlserver_alibi_explain import AlibiExplainRuntime


async def test_anchors(runtime: AlibiExplainRuntime):
    data = np.random.randn(1, 299, 299, 3) * 255
    inference_request = InferenceRequest(
        parameters=Parameters(content_type=NumpyCodec.ContentType),
        inputs=[
            RequestInput(
                name="predict",
                shape=data.shape,
                data=data.tolist(),
                datatype="FP32",
            )
        ],
    )
    response = await runtime.predict(inference_request)

