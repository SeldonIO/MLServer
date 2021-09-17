import base64
from unittest.mock import MagicMock

import numpy as np

from fastapi import Request

from mlserver.codecs import NumpyCodec
from mlserver.types import InferenceRequest, Parameters, RequestInput
from mlserver_alibi_explain import AnchorImageWrapper


async def test_anchors(runtime: AnchorImageWrapper):
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

