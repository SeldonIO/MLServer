"""
Smoke tests for base runtime
"""
from typing import Any, Optional

import numpy as np
import pytest

from mlserver import ModelSettings
from mlserver.codecs import NumpyCodec, StringCodec
from mlserver.types import ResponseOutput, InferenceRequest, InferenceResponse, \
    RequestInput, Parameters
from mlserver_llm.runtime import LLMRuntimeBase, _get_predict_parameters


@pytest.fixture
def input_values() -> dict:
    return {"foo": np.array([[1, 2]], dtype=np.int32), "bar": ["asd", "qwe"]}


@pytest.fixture
def inference_request(input_values: dict) -> InferenceRequest:
    return InferenceRequest(
        inputs=[
            NumpyCodec.encode_input("foo", input_values["foo"]),
            StringCodec.encode_input("bar", input_values["bar"]),
        ]
    )


async def test_runtime_base__smoke(inference_request: InferenceRequest):
    class _DummyModel(LLMRuntimeBase):
        def __init__(self, settings: ModelSettings):
            super().__init__(settings)

        async def _call_impl(
                self, input_data: Any, params: Optional[dict]) -> ResponseOutput:
            return ResponseOutput(
                name="foo", datatype="INT32", shape=[1, 1, 1], data=[1])

    ml = _DummyModel(
        settings=ModelSettings(implementation=str)  # dummy
    )

    res = await ml.predict(inference_request)
    assert isinstance(res, InferenceResponse)


@pytest.mark.parametrize(
    "inference_request, expected_dict",
    [
        (
            InferenceRequest(
                model_name="my-model",
                inputs=[
                    RequestInput(name="foo", datatype="INT32", shape=[1], data=[1]),
                ],
            ),
            {}
        ),
        (
            InferenceRequest(
                model_name="my-model",
                inputs=[
                    RequestInput(name="foo", datatype="INT32", shape=[1], data=[1]),
                ],
                parameters=Parameters(
                    llm_parameters={
                        "threshold": 10,
                        "temperature": 20
                    }
                )
            ),
            {
                "threshold": 10,
                "temperature": 20
            }
        )
    ],
)
def test_get_llm_parameters_from_request(
        inference_request: InferenceRequest, expected_dict: dict):
    params = _get_predict_parameters(inference_request)
    assert params == expected_dict





