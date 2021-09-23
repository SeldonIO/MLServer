import base64
from unittest.mock import MagicMock

import numpy as np

from fastapi import Request

from mlserver.codecs import NumpyCodec
from mlserver.types import InferenceRequest, Parameters, RequestInput
from mlserver_alibi_explain import AnchorImageWrapper
from mlserver_alibi_explain.common import convert_from_bytes, remote_predict


async def test_anchors(runtime: AnchorImageWrapper):
    data = np.random.randn(28, 28, 1) * 255
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
    # TODO: this is really explain
    response = await runtime.predict(inference_request)
    print(convert_from_bytes(response.outputs[0], ty=str))

    # request_mock = MagicMock(Request)
    #
    # async def dummy_request_body():
    #     msg = b'{"x": 2}'
    #     return msg
    #
    # request_mock.body = dummy_request_body
    #
    # explain_response = await runtime.explain(request_mock)
    # print(explain_response)


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
