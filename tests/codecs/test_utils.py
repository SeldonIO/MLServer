import pytest
import numpy as np
import pandas as pd

from typing import Any

from mlserver.types import (
    InferenceRequest,
    InferenceResponse,
    RequestInput,
    Parameters,
    RequestOutput,
    ResponseOutput,
    MetadataTensor,
)
from mlserver.settings import ModelSettings
from mlserver.codecs.errors import CodecError
from mlserver.codecs.utils import (
    decode_inference_request,
    encode_response_output,
    encode_inference_response,
    SingleInputRequestCodec,
    DecodedParameterName,
)
from mlserver.codecs.pandas import PandasCodec
from mlserver.codecs.numpy import NumpyCodec, NumpyRequestCodec
from mlserver.codecs.string import StringCodec


@pytest.mark.parametrize(
    "payload, request_output, expected",
    [
        (
            np.array([1, 2, 3, 4]),
            RequestOutput(name="foo"),
            ResponseOutput(
                name="foo",
                datatype="INT64",
                shape=[4, 1],
                data=[1, 2, 3, 4],
                parameters=Parameters(content_type=NumpyCodec.ContentType),
            ),
        ),
        (
            ["asd"],
            RequestOutput(name="bar"),
            ResponseOutput(
                name="bar",
                datatype="BYTES",
                shape=[1, 1],
                data=[b"asd"],
                parameters=Parameters(content_type=StringCodec.ContentType),
            ),
        ),
        (
            ["2021-02-25T12:00:00Z"],
            RequestOutput(name="bar", parameters=Parameters(content_type="datetime")),
            ResponseOutput(
                name="bar",
                datatype="BYTES",
                shape=[1, 1],
                data=[b"2021-02-25T12:00:00Z"],
                parameters=Parameters(content_type="datetime"),
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
    "payload, expected",
    [
        (
            pd.DataFrame({"a": [1, 2, 3], "b": ["a", "b", "c"]}),
            InferenceResponse(
                model_name="sum-model",
                model_version="v1.2.3",
                parameters=Parameters(content_type=PandasCodec.ContentType),
                outputs=[
                    ResponseOutput(
                        name="a",
                        datatype="INT64",
                        shape=[3, 1],
                        data=[1, 2, 3],
                    ),
                    ResponseOutput(
                        name="b",
                        datatype="BYTES",
                        shape=[3, 1],
                        data=[b"a", b"b", b"c"],
                        parameters=Parameters(content_type=StringCodec.ContentType),
                    ),
                ],
            ),
        ),
        (
            np.array([1, 2, 3]),
            InferenceResponse(
                model_name="sum-model",
                model_version="v1.2.3",
                parameters=Parameters(content_type=NumpyCodec.ContentType),
                outputs=[
                    ResponseOutput(
                        name="output-1",
                        datatype="INT64",
                        shape=[3, 1],
                        data=[1, 2, 3],
                        parameters=Parameters(content_type=NumpyCodec.ContentType),
                    ),
                ],
            ),
        ),
        (
            ["foo", "bar"],
            InferenceResponse(
                model_name="sum-model",
                model_version="v1.2.3",
                parameters=Parameters(content_type=StringCodec.ContentType),
                outputs=[
                    ResponseOutput(
                        name="output-1",
                        datatype="BYTES",
                        shape=[2, 1],
                        data=[b"foo", b"bar"],
                        parameters=Parameters(content_type=StringCodec.ContentType),
                    ),
                ],
            ),
        ),
    ],
)
def test_encode_inference_response(
    payload: Any,
    expected: InferenceResponse,
    sum_model_settings: ModelSettings,
):
    inference_response = encode_inference_response(payload, sum_model_settings)
    assert inference_response == expected


@pytest.mark.parametrize(
    "inference_request, expected",
    [
        (
            InferenceRequest(
                parameters=Parameters(content_type=PandasCodec.ContentType),
                inputs=[
                    RequestInput(
                        name="a",
                        datatype="INT64",
                        shape=[3],
                        data=[1, 2, 3],
                        parameters=Parameters(content_type=NumpyCodec.ContentType),
                    ),
                    RequestInput(
                        name="b",
                        datatype="BYTES",
                        shape=[3],
                        data=[b"a", b"b", b"c"],
                        parameters=Parameters(content_type=StringCodec.ContentType),
                    ),
                ],
            ),
            pd.DataFrame({"a": [1, 2, 3], "b": ["a", "b", "c"]}),
        ),
    ],
)
def test_decode_inference_request(
    inference_request: InferenceRequest,
    expected: Any,
):
    decoded = decode_inference_request(inference_request)

    if isinstance(expected, pd.DataFrame):
        pd.testing.assert_frame_equal(decoded, expected)
    else:
        assert decoded == expected


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
def test_single_input_decode(inference_request: InferenceRequest, expected: np.ndarray):
    inference_request.inputs = [inference_request.inputs[0]]
    first_input = NumpyRequestCodec.decode_request(inference_request)

    np.testing.assert_equal(first_input, expected)


def test_single_input_error(inference_request: InferenceRequest):
    inference_request.inputs.append(
        RequestInput(name="bar", shape=[1, 2], data=[1, 2], datatype="INT32")
    )
    with pytest.raises(CodecError):
        SingleInputRequestCodec.decode_request(inference_request)
