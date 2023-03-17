"""
Smoke tests for base runtime
"""
from typing import Any, Optional

import numpy as np
import pytest

from mlserver import ModelSettings
from mlserver.codecs import NumpyCodec, StringCodec
from mlserver.types import ResponseOutput, InferenceRequest, InferenceResponse
from mlserver_llm.runtime import LLMRuntimeBase


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
        settings=ModelSettings(implementation=str)
    )

    res = await ml.predict(inference_request)
    assert isinstance(res, InferenceResponse)




