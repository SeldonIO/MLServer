import pytest
import numpy as np

from typing import Any, List, Optional

from mlserver.types import InferenceRequest, InferenceResponse, RequestInput
from mlserver.codecs.base import InputCodec
from mlserver.codecs.decorator import SignatureCodec, decode_args
from mlserver.codecs.errors import InputNotFound, OutputNotFound
from mlserver.codecs.numpy import NumpyCodec, NumpyRequestCodec
from mlserver.codecs.string import StringCodec

from ..fixtures import SimpleModel


async def predict_fn(foo: np.ndarray, bar: List[str]) -> np.ndarray:
    return np.array([3])


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


def test_signature_codec(signature_codec: SignatureCodec):
    assert signature_codec._input_codecs == {"foo": NumpyCodec, "bar": StringCodec}
    assert signature_codec._output_codecs == [NumpyCodec]


def test_decode_request(
    signature_codec: SignatureCodec,
    inference_request: InferenceRequest,
    input_values: dict,
):
    inputs = signature_codec.decode_request(inference_request)

    assert len(input_values) == len(inputs)
    np.testing.assert_equal(inputs["foo"], input_values["foo"])
    assert inputs["bar"] == input_values["bar"]


def test_decode_request_not_found(signature_codec: SignatureCodec, inference_request):
    inference_request.inputs[0].name = "not-foo"
    with pytest.raises(InputNotFound) as err:
        signature_codec.decode_request(inference_request)


@pytest.mark.parametrize(
    "output_values, output_codecs",
    [
        (np.array([2]), [NumpyCodec]),
        (["foo"], [StringCodec]),
        ((np.array([2]), ["foo"]), [NumpyCodec, StringCodec]),
        ((["foo"], np.array([2])), [StringCodec, NumpyCodec]),
    ],
)
def test_encode_response(
    signature_codec: SignatureCodec,
    output_values: np.ndarray,
    output_codecs: List[InputCodec],
):
    signature_codec._output_codecs = output_codecs
    response = signature_codec.encode_response(model_name="foo", payload=output_values)

    assert response.model_name == "foo"

    outputs = response.outputs
    assert len(outputs) == len(output_values)
    for idx, output in enumerate(outputs):
        assert output.name == f"output-{idx}"

        codec = output_codecs[idx]
        expected = output_values
        if isinstance(output_values, tuple):
            expected = output_values[idx]
        assert codec.decode_output(output) == expected


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
