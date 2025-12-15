import json
from typing import Any, Dict
from unittest.mock import patch

import alibi.explainers.anchors.anchor_tabular
import numpy as np
import pytest
from alibi.api.interfaces import Explanation
from numpy.testing import assert_array_equal

from mlserver import ModelSettings
from mlserver.codecs import NumpyCodec
from mlserver.types import (
    InferenceRequest,
    InferenceResponse,
    Parameters,
    RequestInput,
    ResponseOutput,
)
from mlserver_alibi_explain.common import (
    convert_from_bytes,
    remote_predict,
    AlibiExplainSettings,
)
from mlserver_alibi_explain.errors import InvalidExplanationShape
from mlserver_alibi_explain.explainers.black_box_runtime import (
    AlibiExplainBlackBoxRuntime,
)
from mlserver_alibi_explain.explainers.integrated_gradients import (
    IntegratedGradientsWrapper,
)
from mlserver_alibi_explain.runtime import AlibiExplainRuntime, AlibiExplainRuntimeBase
from .helpers.run_async import run_async_as_sync, run_sync_as_async

"""
Smoke tests for runtimes
"""


async def test_integrated_gradients__smoke(
    integrated_gradients_runtime: AlibiExplainRuntime,
):
    # TODO: there is an inherit batch as first dimension
    data = np.random.randn(10, 28, 28, 1) * 255
    inference_request = InferenceRequest(
        parameters=Parameters(
            content_type=NumpyCodec.ContentType,
            explain_parameters={
                "baselines": None,
            },
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
    assert isinstance(integrated_gradients_runtime, IntegratedGradientsWrapper)
    response = await integrated_gradients_runtime.predict(inference_request)
    res = convert_from_bytes(response.outputs[0], ty=str)
    res_dict = json.dumps(res)
    assert "meta" in res_dict
    assert "data" in res_dict


async def test_anchors__smoke(
    anchor_image_runtime_with_remote_predict_patch: AlibiExplainRuntime,
):
    data = np.random.randn(1, 28, 28, 1) * 255
    inference_request = InferenceRequest(
        parameters=Parameters(
            content_type=NumpyCodec.ContentType,
            explain_parameters={
                "threshold": 0.95,
                "p_sample": 0.5,
                "tau": 0.25,
            },
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
    assert isinstance(
        anchor_image_runtime_with_remote_predict_patch, AlibiExplainBlackBoxRuntime
    )
    response = await anchor_image_runtime_with_remote_predict_patch.predict(
        inference_request
    )
    res = convert_from_bytes(response.outputs[0], ty=str)
    res_dict = json.dumps(res)
    assert "meta" in res_dict
    assert "data" in res_dict


async def test_remote_predict__smoke(custom_runtime_tf, rest_client):
    def _sync_request(*args, **kwargs):
        kwargs.pop("verify", None)
        return run_async_as_sync(rest_client.post, *args, **kwargs)

    with patch("mlserver_alibi_explain.common.requests") as mock_requests:
        mock_requests.post = _sync_request

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

        endpoint = f"v2/models/{custom_runtime_tf.settings.name}/infer"

        res = await run_sync_as_async(
            remote_predict,
            inference_request,
            predictor_url=endpoint,
            ssl_verify_path="",
        )
        assert isinstance(res, InferenceResponse)


def fake_predictor(x):
    return x


async def test_explain_parameters_pass_through():
    # test that the explain parameters are wired properly, if it runs ok then
    # the assertion is fine
    params = {
        "threshold": 0.95,
    }

    data_np = np.array([[1.0, 2.0]])

    class _DummyExplainer(AlibiExplainRuntimeBase):
        def _explain_impl(
            self, input_data: Any, explain_parameters: Dict
        ) -> Explanation:
            assert explain_parameters == params
            assert_array_equal(input_data, data_np)
            return Explanation(meta={}, data={})

    rt = _DummyExplainer(
        settings=ModelSettings(name="foo", implementation=AlibiExplainRuntime),
        explainer_settings=AlibiExplainSettings(
            infer_uri="dum",
            explainer_type="dum",
            init_parameters=None,
        ),
    )
    rt._model = alibi.explainers.anchors.anchor_tabular.AnchorTabular(
        fake_predictor, ["a"]
    )

    inference_request = InferenceRequest(
        parameters=Parameters(
            content_type=NumpyCodec.ContentType,
            explain_parameters=params,  # this is what we pass through as explain params
        ),
        inputs=[
            RequestInput(
                name="predict",
                shape=data_np.shape,
                data=data_np.tolist(),
                datatype="FP32",
            )
        ],
    )

    res = await rt.predict(inference_request)
    assert isinstance(res, InferenceResponse)


async def test_custom_explain_endpoint(dummy_alibi_explain_client):
    # a test for `/explain` endpoint that returns raw explanation directly
    data = np.random.randn(1, 1)
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

    response = await dummy_alibi_explain_client.post(
        "/explain", json=inference_request.model_dump()
    )
    response_text = json.loads(response.text)
    assert "meta" in response_text
    assert "data" in response_text


@pytest.mark.parametrize(
    "response",
    [
        InferenceResponse(
            model_name="my-model",
            outputs=[
                ResponseOutput(name="foo", datatype="INT32", shape=[1], data=[1]),
                ResponseOutput(name="bar", datatype="INT32", shape=[1], data=[2]),
            ],
        ),
        InferenceResponse(
            model_name="my-model",
            outputs=[
                ResponseOutput(name="foo", datatype="INT32", shape=[1, 1, 1], data=[1]),
            ],
        ),
        InferenceResponse(
            model_name="my-model",
            outputs=[
                ResponseOutput(name="foo", datatype="INT32", shape=[1, 2], data=[1, 2]),
            ],
        ),
    ],
)
async def test_v1_invalid_predict(
    response: InferenceResponse, integrated_gradients_runtime: AlibiExplainRuntime
):
    async def _mocked_predict(request: InferenceRequest) -> InferenceResponse:
        return response

    with patch.object(integrated_gradients_runtime, "predict", _mocked_predict):
        request = InferenceRequest(inputs=[])
        with pytest.raises(InvalidExplanationShape):
            assert isinstance(integrated_gradients_runtime, AlibiExplainRuntimeBase)
            await integrated_gradients_runtime.explain_v1_output(request)
