import pytest
import numpy as np

from typing import List, Optional

from mlserver.types import InferenceRequest, InferenceResponse, RequestInput
from mlserver.codecs.decorator import CodecDecorator, decode_args
from mlserver.codecs.errors import InputNotFound
from mlserver.codecs.numpy import NumpyCodec
from mlserver.codecs.string import StringCodec

from ..fixtures import SumModel


def predict_fn(foo: np.ndarray, bar: List[str]) -> np.ndarray:
    return np.array([2])


@pytest.fixture
def codec_decorator() -> CodecDecorator:
    return CodecDecorator(predict_fn)


@pytest.fixture
def input_values() -> dict:
    return {"foo": np.array([[1, 2]], dtype=np.int32), "bar": ["asd", "qwe"]}


@pytest.fixture
def output_value() -> np.ndarray:
    return np.array([2])


@pytest.fixture
def inference_request(input_values: dict) -> InferenceRequest:
    return InferenceRequest(
        inputs=[
            NumpyCodec.encode_input("foo", input_values["foo"]),
            StringCodec.encode_input("bar", input_values["bar"]),
        ]
    )


def test_codec_decorator(codec_decorator: CodecDecorator):
    assert codec_decorator._input_codecs == {"foo": NumpyCodec, "bar": StringCodec}
    assert codec_decorator._output_codecs == NumpyCodec


def test_get_inputs(
    codec_decorator: CodecDecorator,
    inference_request: InferenceRequest,
    input_values: dict,
):
    inputs = codec_decorator._get_inputs(inference_request)

    assert len(input_values) == len(inputs)
    np.testing.assert_equal(inputs["foo"], input_values["foo"])
    assert inputs["bar"] == input_values["bar"]


def test_get_inputs_not_found(codec_decorator: CodecDecorator, inference_request):
    with pytest.raises(InputNotFound) as err:
        inputs = codec_decorator._get_inputs(inference_request)

    print(err)


def test_decode_args(
    mocker, inference_request: InferenceRequest, output_value: np.ndarray
):
    wrapped_predict_fn = decode_args(predict_fn)
    inference_response = wrapped_predict_fn(inference_request)

    assert isinstance(inference_response, InferenceResponse)

    res = NumpyRequestCodec.decode_response(inference_response)
    assert res == output_value
