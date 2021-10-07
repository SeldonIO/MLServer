import json

import numpy as np
import pytest
import tensorflow as tf
from alibi.saving import load_explainer
from numpy.testing import assert_array_equal

from mlserver import MLModel
from mlserver.codecs import NumpyCodec
from mlserver.types import InferenceRequest, Parameters, RequestInput
from mlserver_alibi_explain import AlibiExplainRuntime
from mlserver_alibi_explain.common import convert_from_bytes
from .conftest import anchor_image_runtime
from .test_model import get_tf_mnist_model_uri


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


@pytest.fixture
async def anchor_image_runtime_with_remote_predict_patch(custom_runtime_tf: MLModel):
    return await anchor_image_runtime(
        custom_runtime_tf,
        "mlserver_alibi_explain.common.remote_predict")


async def test_predict_impl(
        anchor_image_runtime_with_remote_predict_patch: AlibiExplainRuntime,
        custom_runtime_tf: MLModel
):
    # note: custom_runtime_tf is the underlying inference runtime
    # we want to test that the underlying impl predict is functionally correct
    # anchor_image_runtime fixture if already mocking `remote_predict` -> custom_runtime_tf.predict

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
    expected_result_numpy = NumpyCodec.decode_response_output(expected_result.outputs[0])

    assert_array_equal(actual_result, expected_result_numpy)


@pytest.fixture()
def alibi_anchor_image_model():
    inference_model = tf.keras.models.load_model(get_tf_mnist_model_uri())
    model = load_explainer("tests/data/mnist_anchor_image", inference_model.__call__)
    return model


async def test_end_2_end(
        anchor_image_runtime_with_remote_predict_patch: AlibiExplainRuntime,
        alibi_anchor_image_model,
        payload: InferenceRequest
):
    # in this test we are getting explanation and making sure that it the same one as returned by alibi
    # directly
    runtime_result = await anchor_image_runtime_with_remote_predict_patch.predict(payload)
    decoded_runtime_results = json.loads(convert_from_bytes(runtime_result.outputs[0], ty=str))
    alibi_result = alibi_anchor_image_model.explain(NumpyCodec.decode(payload.inputs[0]))

    assert_array_equal(np.array(decoded_runtime_results["data"]["anchor"]), alibi_result.data["anchor"])

