from unittest.mock import patch

import numpy as np
import pytest

from mlserver import MLModel
from mlserver.codecs import NumpyCodec
from mlserver.types import InferenceRequest, Parameters, RequestInput
from mlserver_alibi_explain.common import convert_from_bytes, remote_predict
from mlserver_alibi_explain.runtime import AlibiExplainRuntime
from .conftest import anchor_image_runtime


@pytest.fixture
async def anchor_image_runtime_with_remote_predict_patch(custom_runtime_tf: MLModel):
    return await anchor_image_runtime(
        custom_runtime_tf,
        "mlserver_alibi_explain.common.remote_predict")


async def test_integrated_gradients__smoke(integrated_gradients_runtime: AlibiExplainRuntime):
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
    _ = convert_from_bytes(response.outputs[0], ty=str)


async def test_anchors__smoke(anchor_image_runtime_with_remote_predict_patch: AlibiExplainRuntime):
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
    response = await anchor_image_runtime_with_remote_predict_patch.predict(inference_request)
    _ = convert_from_bytes(response.outputs[0], ty=str)


def test_remote_predict__smoke(runtime_pytorch, rest_client):
    with patch("mlserver_alibi_explain.common.requests") as mock_requests:
        mock_requests.post = rest_client.post

        data = np.random.randn(10, 28, 28, 1) * 255
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

        endpoint = f"v2/models/{runtime_pytorch.settings.name}/infer"

        _ = remote_predict(
            inference_request,
            predictor_url=endpoint)

