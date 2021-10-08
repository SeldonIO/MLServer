from unittest.mock import patch

import numpy as np

from mlserver import ModelSettings, MLModel
from mlserver.codecs import NumpyCodec
from mlserver.types import InferenceRequest, Parameters, RequestInput, MetadataTensor
from mlserver_alibi_explain.common import convert_from_bytes, remote_predict
from mlserver_alibi_explain.runtime import AlibiExplainRuntime

"""
Smoke tests for runtimes
"""


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


async def test_alibi_runtime_wrapper(custom_runtime_tf: MLModel):
    """
    Checks that the wrappers returns back the expected valued from the underlying runtime
    """
    class _MockInit(AlibiExplainRuntime):
        def __init__(self, settings: ModelSettings):
            self._rt = custom_runtime_tf

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

    # settings is dummy and discarded
    wrapper = _MockInit(ModelSettings())

    assert wrapper.settings == custom_runtime_tf.settings
    assert wrapper.name == custom_runtime_tf.name
    assert wrapper.version == custom_runtime_tf.version
    assert wrapper.inputs == custom_runtime_tf.inputs
    assert wrapper.outputs == custom_runtime_tf.outputs
    assert wrapper.ready == custom_runtime_tf.ready

    assert await wrapper.metadata() == await custom_runtime_tf.metadata()
    assert await wrapper.predict(inference_request) == await custom_runtime_tf.predict(inference_request)

    # check setters
    dummy_shape_metadata = [MetadataTensor(
        name="dummy",
        datatype="FP32",
        shape=[1, 2],
    )]
    wrapper.inputs = dummy_shape_metadata
    custom_runtime_tf.inputs = dummy_shape_metadata
    assert wrapper.inputs == custom_runtime_tf.inputs

    wrapper.outputs = dummy_shape_metadata
    custom_runtime_tf.outputs = dummy_shape_metadata
    assert wrapper.outputs == custom_runtime_tf.outputs

    wrapper_public_funcs = list(filter(lambda x: not x.startswith("_"), dir(wrapper)))
    expected_public_funcs = list(filter(lambda x: not x.startswith("_"), dir(custom_runtime_tf)))

    assert wrapper_public_funcs == expected_public_funcs

