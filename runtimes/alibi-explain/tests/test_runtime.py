import numpy as np

from mlserver.codecs import NumpyCodec
from mlserver.types import InferenceRequest, Parameters, RequestInput
from mlserver_alibi_explain.common import convert_from_bytes, remote_predict
from mlserver_alibi_explain.explainers.integrated_gradients import IntegratedGradientsWrapper
from mlserver_alibi_explain.runtime import AlibiExplainRuntime


async def test_integrated_gradients(integrated_gradients_runtime: IntegratedGradientsWrapper):
    # TODO: there is an inherit batch as first dimension
    data = np.random.randn(10, 28, 28, 1) * 255
    inference_request = InferenceRequest(
        parameters=Parameters(
            content_type=NumpyCodec.ContentType,
            explain_parameters={
                "baselines": None,
            }
        ),
        inputs=[
            RequestInput(
                name="predict",
                shape=data.shape,
                data=data.tolist(),
                datatype="FP32",
            )
        ],
    )
    response = await integrated_gradients_runtime.predict(inference_request)
    print(convert_from_bytes(response.outputs[0], ty=str))


async def test_anchors(anchor_image_runtime: AlibiExplainRuntime):
    data = np.random.randn(28, 28, 1) * 255
    inference_request = InferenceRequest(
        parameters=Parameters(
            content_type=NumpyCodec.ContentType,
            explain_parameters={
                "threshold": 0.95,
                "p_sample": 0.5,
                "tau": 0.25,
            }
        ),
        inputs=[
            RequestInput(
                name="predict",
                shape=data.shape,
                data=data.tolist(),
                datatype="FP32",
            )
        ],
    )
    response = await anchor_image_runtime.predict(inference_request)
    print(convert_from_bytes(response.outputs[0], ty=str))


def test_remote_predict__smoke():
    data = np.random.randn(1, 28 * 28) * 255
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
    response = remote_predict(
        inference_request,
        predictor_url="http://localhost:36307/v2/models/test-pytorch-mnist/infer")
    print(response)
