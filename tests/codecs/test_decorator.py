import pytest
import numpy as np

from typing import List, Optional

from mlserver.types import InferenceRequest, InferenceResponse, RequestInput
from mlserver.codecs.decorator import ArgsDecoder, decode_args
from mlserver.codecs.errors import InputNotFound
from mlserver.codecs.numpy import NumpyCodec, NumpyRequestCodec
from mlserver.codecs.string import StringCodec

from ..fixtures import SimpleModel


def predict_fn(foo: np.ndarray, bar: List[str]) -> np.ndarray:
    return np.array([3])


@pytest.fixture
def args_decoder() -> ArgsDecoder:
    return ArgsDecoder(predict_fn)


@pytest.fixture
def input_values() -> dict:
    return {"foo": np.array([[1, 2]], dtype=np.int32), "bar": ["asd", "qwe"]}


@pytest.fixture
def output_value() -> np.ndarray:
    return np.array([3])


@pytest.fixture
def inference_request(input_values: dict) -> InferenceRequest:
    return InferenceRequest(
        inputs=[
            NumpyCodec.encode_input("foo", input_values["foo"]),
            StringCodec.encode_input("bar", input_values["bar"]),
        ]
    )


def test_args_decoder(args_decoder: ArgsDecoder):
    assert args_decoder._input_codecs == {"foo": NumpyCodec, "bar": StringCodec}
    assert args_decoder._output_codecs == NumpyCodec


def test_get_inputs(
    args_decoder: ArgsDecoder,
    inference_request: InferenceRequest,
    input_values: dict,
):
    inputs = args_decoder.get_inputs(inference_request)

    assert len(input_values) == len(inputs)
    np.testing.assert_equal(inputs["foo"], input_values["foo"])
    assert inputs["bar"] == input_values["bar"]


def test_get_inputs_not_found(args_decoder: ArgsDecoder, inference_request):
    with pytest.raises(InputNotFound) as err:
        inputs = args_decoder.get_inputs(inference_request)

    print(err)


async def test_decode_args(
    simple_model: SimpleModel,
    inference_request: InferenceRequest,
    output_value: np.ndarray,
):
    inference_response = await simple_model.predict(inference_request)

    assert isinstance(inference_response, InferenceResponse)

    res = NumpyRequestCodec.decode_response(inference_response)
    assert res == output_value
