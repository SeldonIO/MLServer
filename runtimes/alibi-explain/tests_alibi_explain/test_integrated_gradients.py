import json
from typing import Tuple

import numpy as np
import pytest
import tensorflow as tf
from alibi.explainers import IntegratedGradients
from numpy.testing import assert_array_almost_equal

from mlserver.codecs import NumpyCodec
from mlserver.types import InferenceRequest, Parameters, RequestInput
from mlserver_alibi_explain.common import convert_from_bytes


@pytest.fixture()
def payload() -> InferenceRequest:
    data = np.random.randn(1, 28, 28, 1) * 255

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


@pytest.fixture()
def alibi_integrated_gradients_model(tf_mnist_model_uri: str) -> Tuple:
    inference_model = tf.keras.models.load_model(tf_mnist_model_uri)
    ig_model = IntegratedGradients(model=inference_model)
    return inference_model, ig_model


async def test_end_2_end(
    integrated_gradients_runtime,
    alibi_integrated_gradients_model,
    payload: InferenceRequest,
):
    # in this test we are getting explanation and making sure that it the same
    # one as returned by alibi
    # directly
    runtime_result = await integrated_gradients_runtime.predict(payload)
    decoded_runtime_results = json.loads(
        convert_from_bytes(runtime_result.outputs[0], ty=str)
    )

    # get the data as numpy from the inference request payload
    infer_model, ig_model = alibi_integrated_gradients_model
    input_data_np = NumpyCodec.decode_input(payload.inputs[0])
    predictions = infer_model(input_data_np).numpy().argmax(axis=1)
    alibi_result = ig_model.explain(input_data_np, target=predictions)

    assert_array_almost_equal(
        np.array(decoded_runtime_results["data"]["attributions"]),
        alibi_result.data["attributions"],
    )
