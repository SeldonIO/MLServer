import numpy as np
import pytest
from numpy.testing import assert_array_equal

from mlserver import MLModel
from mlserver.codecs import NumpyCodec
from mlserver.types import InferenceRequest, Parameters, RequestInput
from mlserver_alibi_explain import AlibiExplainRuntime
from .conftest import anchor_image_runtime


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


