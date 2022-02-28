import pytest
import numpy as np

from typing import Any

from mlserver.types import (
    InferenceRequest,
    RequestInput,
    Parameters,
    RequestOutput,
    ResponseOutput,
    MetadataTensor,
)
from mlserver.codecs.base import CodecError
from mlserver.codecs.utils import (
    encode_response_output,
    FirstInputRequestCodec,
    DecodedParameterName,
)
from mlserver.codecs.numpy import NumpyRequestCodec


@pytest.mark.parametrize(
    "payload, request_output, expected",
    [
        (
            np.array([1, 2, 3, 4]),
            RequestOutput(name="foo"),
            ResponseOutput(name="foo", datatype="INT64", shape=[4], data=[1, 2, 3, 4]),
        ),
        (
            ["asd"],
            RequestOutput(name="bar"),
            ResponseOutput(name="bar", datatype="BYTES", shape=[1], data=[b"asd"]),
        ),
        (
            ["2021-02-25T12:00:00Z"],
            RequestOutput(name="bar", parameters=Parameters(content_type="datetime")),
            ResponseOutput(
                name="bar", datatype="BYTES", shape=[1], data=[b"2021-02-25T12:00:00Z"]
            ),
        ),
        ({1, 2, 3, 4}, RequestOutput(name="bar"), None),
    ],
)
def test_encode_response_output(
    payload: Any, request_output: RequestOutput, expected: ResponseOutput
):
    metadata_outputs = {
        "foo": MetadataTensor(
            name="foo",
            datatype="INT32",
            shape=[-1],
            parameters=Parameters(content_type="np"),
        )
    }
    response_output = encode_response_output(payload, request_output, metadata_outputs)
    assert response_output == expected


@pytest.mark.parametrize(
    "inference_request, expected",
    [
        (
            InferenceRequest(
                inputs=[
                    RequestInput(
                        name="foo", shape=[2, 2], data=[1, 2, 3, 4], datatype="INT32"
                    )
                ]
            ),
            np.array([[1, 2], [3, 4]]),
        ),
        (
            InferenceRequest(
                inputs=[
                    RequestInput(
                        name="foo",
                        shape=[2, 2],
                        data=[1, 2, 3, 4],
                        datatype="INT32",
                        parameters=Parameters(**{DecodedParameterName: np.array([23])}),
                    )
                ]
            ),
            np.array([23]),
        ),
    ],
)
def test_first_input_decode(inference_request: InferenceRequest, expected: np.ndarray):
    inference_request.inputs = [inference_request.inputs[0]]
    first_input = NumpyRequestCodec.decode(inference_request)

    np.testing.assert_equal(first_input, expected)


def test_first_input_error(inference_request: InferenceRequest):
    inference_request.inputs.append(
        RequestInput(name="bar", shape=[1, 2], data=[1, 2], datatype="INT32")
    )
    with pytest.raises(CodecError):
        FirstInputRequestCodec.decode(inference_request)
