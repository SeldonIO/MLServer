import pytest
import numpy as np

from typing import List, Optional

from mlserver.types import InferenceRequest, InferenceResponse, RequestInput
from mlserver.codecs.decorator import CodecDecorator
from mlserver.codecs.errors import InputNotFound
from mlserver.codecs.numpy import NumpyCodec
from mlserver.codecs.string import StringCodec

from ..fixtures import SumModel


def predict_fn(foo: np.ndarray, bar: List[str]) -> np.ndarray:
    return np.array([2])


@pytest.fixture
def codec_decorator() -> CodecDecorator:
    return CodecDecorator(predict_fn)


def test_codec_decorator(codec_decorator: CodecDecorator):
    assert codec_decorator._input_codecs == {"foo": NumpyCodec, "bar": StringCodec}
    assert codec_decorator._output_codecs == NumpyCodec


def test_get_inputs(codec_decorator: CodecDecorator):
    inference_request = InferenceRequest(
        inputs=[
            RequestInput(name="foo", datatype="INT32", shape=[1, 2], data=[1, 2]),
            RequestInput(
                name="bar", datatype="BYTES", shape=[1, 2], data=["asd", "qwe"]
            ),
        ]
    )
    expected = {"foo": np.array([[1, 2]], dtype=np.int32), "bar": ["asd", "qwe"]}

    inputs = codec_decorator._get_inputs(inference_request)

    assert len(expected) == len(inputs)
    np.testing.assert_equal(inputs["foo"], expected["foo"])
    assert inputs["bar"] == expected["bar"]


def test_get_inputs_not_found(codec_decorator: CodecDecorator):
    inference_request = InferenceRequest(
        inputs=[
            RequestInput(name="foo", datatype="INT32", shape=[1, 2], data=[1, 2]),
            RequestInput(
                name="wrong",
                datatype="BYTES",
                shape=[1, 2],
                data=["asd", "qwe"],
            ),
        ]
    )

    with pytest.raises(InputNotFound) as err:
        inputs = codec_decorator._get_inputs(inference_request)

    print(err)


def test_decode_args():
    predict = CodecDecorator(SumModel.predict)
    print(predict)
