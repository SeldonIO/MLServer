import json
import os
from pathlib import Path

import numpy as np
import pytest
import tensorflow as tf
from alibi.saving import load_explainer
from numpy.testing import assert_array_equal

from mlserver import MLModel
from mlserver.codecs import NumpyCodec, StringCodec
from mlserver.types import InferenceRequest, Parameters, RequestInput
from mlserver_alibi_explain import AlibiExplainRuntime
from mlserver_alibi_explain.common import convert_from_bytes
from helpers.tf_model import get_tf_mnist_model_uri
from mlserver_alibi_explain.explainers.black_box_runtime import _v2_inference_request

TESTS_PATH = Path(os.path.dirname(__file__))


@pytest.fixture
def payload() -> InferenceRequest:
    data = np.random.randn(28, 28, 1) * 255

    # now we go via the inference model and see if we get the same results
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
    return inference_request


async def test_predict_impl(
    anchor_image_runtime_with_remote_predict_patch: AlibiExplainRuntime,
    custom_runtime_tf: MLModel,
):
    # note: custom_runtime_tf is the underlying inference runtime
    # we want to test that the underlying impl predict is functionally correct
    # anchor_image_runtime fixture is already mocking
    # `remote_predict` -> custom_runtime_tf.predict

    # [batch, image_x, image_y, channel]
    data = np.random.randn(10, 28, 28, 1) * 255
    actual_result = anchor_image_runtime_with_remote_predict_patch._rt._infer_impl(data)

    # now we go via the inference model and see if we get the same results
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
    expected_result = await custom_runtime_tf.predict(inference_request)
    expected_result_numpy = NumpyCodec.decode_response_output(
        expected_result.outputs[0]
    )

    assert_array_equal(actual_result, expected_result_numpy)


@pytest.fixture()
def alibi_anchor_image_model():
    inference_model = tf.keras.models.load_model(get_tf_mnist_model_uri())
    model = load_explainer(
        TESTS_PATH / "data" / "mnist_anchor_image", inference_model.__call__
    )
    return model


async def test_end_2_end(
    anchor_image_runtime_with_remote_predict_patch: AlibiExplainRuntime,
    alibi_anchor_image_model,
    payload: InferenceRequest,
):
    # in this test we are getting explanation and making sure that it the same one
    # as returned by alibi directly
    runtime_result = await anchor_image_runtime_with_remote_predict_patch.predict(
        payload
    )
    decoded_runtime_results = json.loads(
        convert_from_bytes(runtime_result.outputs[0], ty=str)
    )
    alibi_result = alibi_anchor_image_model.explain(
        NumpyCodec.decode(payload.inputs[0])
    )

    assert_array_equal(
        np.array(decoded_runtime_results["data"]["anchor"]), alibi_result.data["anchor"]
    )


@pytest.mark.parametrize(
    "payload, expected_v2_request",
    [
        # numpy payload
        (
            np.zeros([2, 4]),
            InferenceRequest(
                parameters=Parameters(content_type=NumpyCodec.ContentType),
                inputs=[
                    RequestInput(
                        parameters=Parameters(content_type=NumpyCodec.ContentType),
                        name="predict",
                        data=np.zeros([2, 4]).flatten().tolist(),
                        shape=[2, 4],
                        datatype="FP64",  # default for np.zeros
                    )
                ],
            ),
        ),
        # List[str] payload
        (
            ["dummy text"],
            InferenceRequest(
                parameters=Parameters(content_type=StringCodec.ContentType),
                inputs=[
                    RequestInput(
                        parameters=Parameters(content_type=StringCodec.ContentType),
                        name="predict",
                        data="dummy text",
                        shape=[1, 10],
                        datatype="BYTES",
                    )
                ],
            ),
        ),
    ],
)
def test_encode_inference_request__as_expected(payload, expected_v2_request):
    encoded_request = _v2_inference_request(payload)
    assert encoded_request == expected_v2_request
