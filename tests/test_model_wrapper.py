import numpy as np
import pytest

from mlserver import MLModel, ModelSettings
from mlserver.codecs import StringCodec, NumpyCodec
from mlserver.model_wrapper import WrapperMLModel
from mlserver.types import InferenceRequest, MetadataTensor


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


async def test_model_wrapper(
    simple_model: MLModel, inference_request: InferenceRequest
):
    """
    Checks that the wrapper returns back the expected valued from the underlying rt
    """

    class _MockInit(WrapperMLModel):
        def __init__(self, settings: ModelSettings):
            self._rt = simple_model

    # settings object is dummy and discarded
    wrapper = _MockInit(ModelSettings(name="foo", implementation=WrapperMLModel))

    assert wrapper.settings == simple_model.settings
    assert wrapper.name == simple_model.name
    assert wrapper.version == simple_model.version
    assert wrapper.inputs == simple_model.inputs
    assert wrapper.outputs == simple_model.outputs
    assert wrapper.ready == simple_model.ready

    assert await wrapper.metadata() == await simple_model.metadata()
    assert await wrapper.predict(inference_request) == await simple_model.predict(
        inference_request
    )

    # check setters
    dummy_shape_metadata = [
        MetadataTensor(
            name="dummy",
            datatype="FP32",
            shape=[1, 2],
        )
    ]
    wrapper.inputs = dummy_shape_metadata
    simple_model.inputs = dummy_shape_metadata
    assert wrapper.inputs == simple_model.inputs

    wrapper.outputs = dummy_shape_metadata
    simple_model.outputs = dummy_shape_metadata
    assert wrapper.outputs == simple_model.outputs

    wrapper_public_funcs = list(filter(lambda x: not x.startswith("_"), dir(wrapper)))
    expected_public_funcs = list(
        filter(lambda x: not x.startswith("_"), dir(simple_model))
    )

    assert wrapper_public_funcs == expected_public_funcs
