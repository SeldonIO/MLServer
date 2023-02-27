import json
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

import numpy as np
import pytest
import tensorflow as tf
from alibi.saving import load_explainer
from numpy.testing import assert_allclose

from mlserver import MLModel
from mlserver.codecs import NumpyCodec, StringCodec
from mlserver.types import (
    InferenceRequest,
    Parameters,
    RequestInput,
    MetadataModelResponse,
    MetadataTensor,
    RequestOutput,
)
from mlserver_alibi_explain import AlibiExplainRuntime
from mlserver_alibi_explain.common import (
    convert_from_bytes,
    to_v2_inference_request,
    _DEFAULT_INPUT_NAME,
)

from .helpers.run_async import run_sync_as_async
from .helpers.tf_model import get_tf_mnist_model_uri

TESTS_PATH = Path(os.path.dirname(__file__))
_DEFAULT_ID_NAME = "dummy_id"


@pytest.fixture
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
    actual_result = await run_sync_as_async(
        anchor_image_runtime_with_remote_predict_patch._rt._infer_impl, data
    )

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
    expected_result_numpy = NumpyCodec.decode_output(expected_result.outputs[0])

    assert_allclose(actual_result, expected_result_numpy, rtol=1, atol=250)


@pytest.fixture()
def alibi_anchor_image_model(anchor_image_directory):
    inference_model = tf.keras.models.load_model(get_tf_mnist_model_uri())
    model = load_explainer(anchor_image_directory, inference_model.predict)
    return model


async def test_end_2_end(
    anchor_image_runtime_with_remote_predict_patch: AlibiExplainRuntime,
    alibi_anchor_image_model,
    payload: InferenceRequest,
):
    # in this test we are getting explanation and making sure that is the same one
    # as returned by alibi directly
    runtime_result = await anchor_image_runtime_with_remote_predict_patch.predict(
        payload
    )
    decoded_runtime_results = json.loads(
        convert_from_bytes(runtime_result.outputs[0], ty=str)
    )
    alibi_result = alibi_anchor_image_model.explain(
        NumpyCodec.decode_input(payload.inputs[0])[0]  # payload has batch dimension,
        # we remove it for alibi
    )

    assert_allclose(
        np.array(decoded_runtime_results["data"]["anchor"]),
        alibi_result.data["anchor"],
        rtol=1,
        atol=250,
    )


async def test_end_2_end_explain_v1_output(
    anchor_image_runtime_with_remote_predict_patch: AlibiExplainRuntime,
    alibi_anchor_image_model,
    payload: InferenceRequest,
):
    # in this test we get raw explanation as opposed to v2

    response = (
        await anchor_image_runtime_with_remote_predict_patch._rt.explain_v1_output(
            payload
        )
    )

    response_body = json.loads(response.body)
    assert "meta" in response_body
    assert "data" in response_body


@pytest.mark.parametrize(
    "payload, metadata, output, expected_v2_request",
    [
        # numpy payload
        (
            np.zeros([2, 4]),
            None,
            None,
            InferenceRequest(
                id=_DEFAULT_ID_NAME,
                parameters=Parameters(content_type=NumpyCodec.ContentType),
                inputs=[
                    RequestInput(
                        parameters=Parameters(content_type=NumpyCodec.ContentType),
                        name=_DEFAULT_INPUT_NAME,
                        data=np.zeros([2, 4]).flatten().tolist(),
                        shape=[2, 4],
                        datatype="FP64",  # default for np.zeros
                    )
                ],
                outputs=[],
            ),
        ),
        # numpy with metadata
        (
            np.zeros([2, 4]),
            MetadataModelResponse(
                name="dummy",
                platform="dummy",
                inputs=[MetadataTensor(name="input_name", datatype="dummy", shape=[])],
                outputs=[
                    MetadataTensor(name="output_name", datatype="dummy", shape=[])
                ],
            ),
            None,
            InferenceRequest(
                id=_DEFAULT_ID_NAME,
                parameters=Parameters(content_type=NumpyCodec.ContentType),
                inputs=[
                    RequestInput(
                        parameters=Parameters(content_type=NumpyCodec.ContentType),
                        name="input_name",  # inserted from metadata above
                        data=np.zeros([2, 4]).flatten().tolist(),
                        shape=[2, 4],
                        datatype="FP64",  # default for np.zeros
                    )
                ],
                outputs=[
                    RequestOutput(name="output_name")
                ],  # inserted from metadata above
            ),
        ),
        # multiple outputs in the metadata, return only the first output
        (
                np.zeros([2, 4]),
                MetadataModelResponse(
                    name="dummy",
                    platform="dummy",
                    inputs=[
                        MetadataTensor(name="input_name", datatype="dummy", shape=[])],
                    outputs=[
                        MetadataTensor(name="output_name", datatype="dummy", shape=[]),
                        MetadataTensor(name="output_name_2", datatype="dummy", shape=[])
                    ],
                ),
                None,
                InferenceRequest(
                    id=_DEFAULT_ID_NAME,
                    parameters=Parameters(content_type=NumpyCodec.ContentType),
                    inputs=[
                        RequestInput(
                            parameters=Parameters(content_type=NumpyCodec.ContentType),
                            name="input_name",  # inserted from metadata above
                            data=np.zeros([2, 4]).flatten().tolist(),
                            shape=[2, 4],
                            datatype="FP64",  # default for np.zeros
                        )
                    ],
                    outputs=[
                        RequestOutput(name="output_name"),
                    ],  # inserted from metadata above
                ),
        ),
        # Specified output
        (
                np.zeros([2, 4]),
                None,
                "output_name",
                InferenceRequest(
                    id=_DEFAULT_ID_NAME,
                    parameters=Parameters(content_type=NumpyCodec.ContentType),
                    inputs=[
                        RequestInput(
                            parameters=Parameters(content_type=NumpyCodec.ContentType),
                            name=_DEFAULT_INPUT_NAME,
                            data=np.zeros([2, 4]).flatten().tolist(),
                            shape=[2, 4],
                            datatype="FP64",  # default for np.zeros
                        )
                    ],
                    outputs=[
                        RequestOutput(name="output_name"),
                    ],  # inserted from output
                ),
        ),
        # Specified output and metadata
        (
                np.zeros([2, 4]),
                MetadataModelResponse(
                    name="dummy",
                    platform="dummy",
                    inputs=[
                        MetadataTensor(name="input_name", datatype="dummy", shape=[])],
                    outputs=[
                        MetadataTensor(name="output_name", datatype="dummy", shape=[]),
                        MetadataTensor(name="output_name_2", datatype="dummy", shape=[])
                    ],
                ),
                "output_name_2",
                InferenceRequest(
                    id=_DEFAULT_ID_NAME,
                    parameters=Parameters(content_type=NumpyCodec.ContentType),
                    inputs=[
                        RequestInput(
                            parameters=Parameters(content_type=NumpyCodec.ContentType),
                            name="input_name",  # from metadata
                            data=np.zeros([2, 4]).flatten().tolist(),
                            shape=[2, 4],
                            datatype="FP64",  # default for np.zeros
                        )
                    ],
                    outputs=[
                        RequestOutput(name="output_name_2"),
                    ],  # from output
                ),
        ),
        # List[str] payload
        (
            ["dummy", "dummy text"],
            None,
            None,
            InferenceRequest(
                id=_DEFAULT_ID_NAME,
                parameters=Parameters(content_type=StringCodec.ContentType),
                inputs=[
                    RequestInput(
                        parameters=Parameters(content_type=StringCodec.ContentType),
                        name=_DEFAULT_INPUT_NAME,
                        data=["dummy", "dummy text"],
                        shape=[2, 1],
                        datatype="BYTES",
                    )
                ],
                outputs=[],
            ),
        ),
    ],
)
@patch(
    "mlserver_alibi_explain.common.generate_uuid",
    MagicMock(return_value=_DEFAULT_ID_NAME),
)
def test_encode_inference_request__as_expected(
        payload, metadata, output, expected_v2_request):
    encoded_request = to_v2_inference_request(payload, metadata, output)
    assert encoded_request == expected_v2_request
