import pytest
import numpy as np
import pandas as pd

from typing import Any, Callable, Dict, Optional, List, Tuple

from mlserver.types import (
    InferenceRequest,
    InferenceResponse,
    RequestInput,
    ResponseOutput,
    Parameters,
)
from mlserver.codecs.base import InputCodec
from mlserver.codecs.utils import Codec
from mlserver.codecs.decorator import SignatureCodec, _as_list
from mlserver.codecs.errors import InputsNotFound, OutputNotFound
from mlserver.codecs.numpy import NumpyCodec, NumpyRequestCodec
from mlserver.codecs.string import StringCodec
from mlserver.codecs.pandas import PandasCodec

from ..fixtures import SimpleModel


async def predict_fn(foo: np.ndarray, bar: List[str]) -> np.ndarray:
    return np.array([3])


def _implicit_optional(foo: np.ndarray, bar: List[str] = None) -> np.ndarray:
    return np.array([2])


def _explicit_optional(foo: np.ndarray, bar: Optional[List[str]]) -> np.ndarray:
    return np.array([2])


@pytest.fixture
def signature_codec() -> SignatureCodec:
    return SignatureCodec(predict_fn)


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


def test_get_codecs(signature_codec: SignatureCodec):
    assert signature_codec._input_codecs == {"foo": NumpyCodec, "bar": StringCodec}
    assert signature_codec._output_codecs == [NumpyCodec]


def test_get_codecs_with_request():
    def _f(foo: pd.DataFrame) -> (np.ndarray, pd.DataFrame):
        return np.array([2]), pd.DataFrame({"bar": [2]})

    signature_codec = SignatureCodec(_f)
    assert signature_codec._input_codecs == {"foo": PandasCodec}
    assert signature_codec._output_codecs == [NumpyCodec, PandasCodec]


@pytest.mark.parametrize("predict_fn", [_implicit_optional, _explicit_optional])
def test_get_codecs_with_optional(predict_fn: Callable):
    signature_codec = SignatureCodec(predict_fn)
    assert signature_codec._input_codecs == {"foo": NumpyCodec, "bar": StringCodec}
    assert signature_codec._output_codecs == [NumpyCodec]


@pytest.mark.parametrize(
    "request_inputs, input_codecs, expected_values",
    [
        (
            [
                RequestInput(name="foo", datatype="INT64", shape=[1], data=[2]),
                RequestInput(name="bar", datatype="BYTES", shape=[1], data=[b"asd"]),
            ],
            {"foo": NumpyCodec, "bar": StringCodec},
            {"foo": np.array([2]), "bar": ["asd"]},
        ),
        (
            [
                RequestInput(name="a", datatype="INT64", shape=[1], data=[2]),
                RequestInput(name="b", datatype="BYTES", shape=[1], data=["asd"]),
            ],
            {"foo": PandasCodec},
            {"foo": pd.DataFrame({"a": [2], "b": ["asd"]})},
        ),
        (
            [
                RequestInput(name="bar", datatype="BYTES", shape=[1], data=[b"fiu"]),
                RequestInput(name="a", datatype="INT64", shape=[1], data=[2]),
                RequestInput(name="b", datatype="BYTES", shape=[1], data=["asd"]),
            ],
            {"bar": StringCodec, "foo": PandasCodec},
            {"bar": ["fiu"], "foo": pd.DataFrame({"a": [2], "b": ["asd"]})},
        ),
    ],
)
def test_decode_request(
    signature_codec: SignatureCodec,
    request_inputs: List[RequestInput],
    input_codecs: Dict[str, Codec],
    expected_values: dict,
):
    signature_codec._input_codecs = input_codecs

    inference_request = InferenceRequest(inputs=request_inputs)
    inputs = signature_codec.decode_request(inference_request)

    assert len(inputs) == len(expected_values)
    for key, value in inputs.items():
        assert key in expected_values
        expected_value = expected_values[key]

        if isinstance(expected_value, pd.DataFrame):
            pd.testing.assert_frame_equal(value, expected_value)
        else:
            assert value == expected_value


def test_decode_request_not_found(
    signature_codec: SignatureCodec, inference_request: InferenceRequest
):
    inference_request.inputs[0].name = "not-foo"
    with pytest.raises(InputsNotFound):
        signature_codec.decode_request(inference_request)


@pytest.mark.parametrize(
    "output_values, output_codecs, expected_outputs",
    [
        (
            np.array([2]),
            [NumpyCodec],
            [
                ResponseOutput(
                    name="output-0",
                    datatype="INT64",
                    shape=[1, 1],
                    data=[2],
                    parameters=Parameters(content_type=NumpyCodec.ContentType),
                )
            ],
        ),
        (
            ["foo"],
            [StringCodec],
            [
                ResponseOutput(
                    name="output-0",
                    datatype="BYTES",
                    shape=[1, 1],
                    data=[b"foo"],
                    parameters=Parameters(content_type=StringCodec.ContentType),
                )
            ],
        ),
        (
            (np.array([2]), ["foo"]),
            [NumpyCodec, StringCodec],
            [
                ResponseOutput(
                    name="output-0",
                    datatype="INT64",
                    shape=[1, 1],
                    data=[2],
                    parameters=Parameters(content_type=NumpyCodec.ContentType),
                ),
                ResponseOutput(
                    name="output-1",
                    datatype="BYTES",
                    shape=[1, 1],
                    data=[b"foo"],
                    parameters=Parameters(content_type=StringCodec.ContentType),
                ),
            ],
        ),
        (
            (["foo"], np.array([2])),
            [StringCodec, NumpyCodec],
            [
                ResponseOutput(
                    name="output-0",
                    datatype="BYTES",
                    shape=[1, 1],
                    data=[b"foo"],
                    parameters=Parameters(content_type=StringCodec.ContentType),
                ),
                ResponseOutput(
                    name="output-1",
                    datatype="INT64",
                    shape=[1, 1],
                    data=[2],
                    parameters=Parameters(content_type=NumpyCodec.ContentType),
                ),
            ],
        ),
        (
            pd.DataFrame({"a": [2], "b": ["foo"]}),
            [PandasCodec],
            [
                ResponseOutput(name="a", datatype="INT64", shape=[1, 1], data=[2]),
                ResponseOutput(
                    name="b",
                    datatype="BYTES",
                    shape=[1, 1],
                    data=[b"foo"],
                    parameters=Parameters(content_type=StringCodec.ContentType),
                ),
            ],
        ),
        (
            (pd.DataFrame({"a": [2], "b": ["foo"]}), ["bar"]),
            [PandasCodec, StringCodec],
            [
                ResponseOutput(name="a", datatype="INT64", shape=[1, 1], data=[2]),
                ResponseOutput(
                    name="b",
                    datatype="BYTES",
                    shape=[1, 1],
                    data=[b"foo"],
                    parameters=Parameters(content_type=StringCodec.ContentType),
                ),
                ResponseOutput(
                    name="output-1",
                    datatype="BYTES",
                    shape=[1, 1],
                    data=[b"bar"],
                    parameters=Parameters(content_type=StringCodec.ContentType),
                ),
            ],
        ),
        (
            (np.array([3]), pd.DataFrame({"a": [2], "b": ["foo"]})),
            [NumpyCodec, PandasCodec],
            [
                ResponseOutput(
                    name="output-0",
                    datatype="INT64",
                    shape=[1, 1],
                    data=[3],
                    parameters=Parameters(content_type=NumpyCodec.ContentType),
                ),
                ResponseOutput(name="a", datatype="INT64", shape=[1, 1], data=[2]),
                ResponseOutput(
                    name="b",
                    datatype="BYTES",
                    shape=[1, 1],
                    data=[b"foo"],
                    parameters=Parameters(content_type=StringCodec.ContentType),
                ),
            ],
        ),
    ],
)
def test_encode_response(
    signature_codec: SignatureCodec,
    output_values: np.ndarray,
    output_codecs: List[InputCodec],
    expected_outputs: List[ResponseOutput],
):
    signature_codec._output_codecs = output_codecs
    response = signature_codec.encode_response(model_name="foo", payload=output_values)

    assert response.model_name == "foo"
    assert response.outputs == expected_outputs


@pytest.mark.parametrize(
    "invalid_values",
    [
        ("foo", np.array([2])),
        (np.array([2]), "foo"),
    ],
)
def test_encode_response_not_found(
    signature_codec: SignatureCodec, invalid_values: List[Any]
):
    """
    Ensure the `SignatureCodec` detects when an output does not match the
    method's signature and raise an error.
    """
    with pytest.raises(OutputNotFound):
        signature_codec.encode_response(model_name="foo", payload=invalid_values)


async def test_decode_args(
    simple_model: SimpleModel,
    inference_request: InferenceRequest,
    output_value: np.ndarray,
):
    inference_response = await simple_model.predict(inference_request)

    assert isinstance(inference_response, InferenceResponse)

    res = NumpyRequestCodec.decode_response(inference_response)
    assert res == output_value


def test_as_list_typing_tuple():
    signature_list = _as_list(Tuple[np.ndarray, np.ndarray])
    assert signature_list == [np.ndarray, np.ndarray]


def test_as_list_native_tuple():
    signature_list = _as_list((np.ndarray, np.ndarray))
    assert signature_list == [np.ndarray, np.ndarray]
