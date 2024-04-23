import pytest
import inspect
import numpy as np
import pandas as pd

from typing import Any, Optional

from mlserver.types import InferenceRequest, RequestInput, Parameters, TensorData
from mlserver.codecs import RequestCodec, NumpyCodec, StringCodec
from mlserver.codecs.numpy import NumpyRequestCodec
from mlserver.codecs.pandas import PandasCodec
from mlserver.model import MLModel

from .fixtures import TextModel, TextStreamModel


async def test_generate_stream_fallback(
    text_model: TextModel,
    generate_request: InferenceRequest,
):
    generator = text_model.generate_stream(generate_request)
    assert inspect.isasyncgen(generator)

    responses = []
    async for response in generator:
        responses.append(response)

    assert len(responses) == 1
    assert len(responses[0].outputs) > 0


async def test_generate_stream(
    text_stream_model: TextStreamModel,
    generate_request: InferenceRequest,
):
    generator = text_stream_model.generate_stream(generate_request)
    assert inspect.isasyncgen(generator)

    responses = []
    async for response in generator:
        responses.append(response)

    ref_text = ["What", " is", " the", " capital", " of", " France?"]
    assert len(responses) == len(ref_text)

    for idx in range(len(ref_text)):
        assert ref_text[idx] == StringCodec.decode_output(responses[idx].outputs[0])[0]


@pytest.mark.parametrize(
    "request_input,expected",
    [
        (
            RequestInput(
                name="foo",
                shape=[2, 2],
                data=[1, 2, 3, 4],
                datatype="INT32",
                parameters=Parameters(
                    content_type=NumpyCodec.ContentType,
                    _decoded_payload=np.array([[1, 2], [3, 4]]),
                ),
            ),
            np.array([[1, 2], [3, 4]]),
        ),
        (
            RequestInput(
                name="foo",
                shape=[17],
                data=b"my unicode string",
                datatype="BYTES",
                parameters=Parameters(
                    content_type=StringCodec.ContentType,
                    _decoded_payload="my unicode string",
                ),
            ),
            ["my unicode string"],
        ),
        (
            RequestInput(
                name="bar",
                shape=[2],
                data=[1, 2],
                datatype="FP32",
                parameters=Parameters(_decoded_payload=None),
            ),
            None,
        ),
        (
            RequestInput(
                name="bar",
                shape=[2],
                data=[1, 2],
                datatype="FP32",
                parameters=Parameters(),
            ),
            TensorData(root=[1, 2]),
        ),
        (
            RequestInput(
                name="bar",
                shape=[2],
                data=[1, 2],
                datatype="FP32",
            ),
            TensorData(root=[1, 2]),
        ),
    ],
)
def test_decode(sum_model: MLModel, request_input: RequestInput, expected: Any):
    decoded = sum_model.decode(request_input)

    if isinstance(expected, np.ndarray):
        np.testing.assert_array_equal(decoded, expected)  # type: ignore
    else:
        assert decoded == expected  # type: ignore


@pytest.mark.parametrize(
    "inference_request, expected, default_codec",
    [
        # Request with no content type
        (
            InferenceRequest(
                inputs=[
                    RequestInput(
                        name="bar",
                        shape=[2],
                        data=[1, 2],
                        datatype="FP32",
                    )
                ]
            ),
            InferenceRequest(
                inputs=[
                    RequestInput(
                        name="bar",
                        shape=[2],
                        data=[1, 2],
                        datatype="FP32",
                    )
                ]
            ),
            None,
        ),
        # Request with no content type BUT a default codec
        (
            InferenceRequest(
                inputs=[
                    RequestInput(
                        name="bar",
                        shape=[2],
                        data=[1, 2],
                        datatype="FP32",
                    )
                ]
            ),
            np.array([1, 2], dtype=float),
            NumpyRequestCodec,
        ),
        # Request with a content type
        (
            InferenceRequest(
                parameters=Parameters(content_type="np"),
                inputs=[
                    RequestInput(
                        name="bar",
                        shape=[2],
                        data=[1, 2],
                        datatype="FP32",
                    )
                ],
            ),
            np.array([1, 2], dtype=float),
            None,
        ),
        # Request with a content type AND a default codec
        (
            InferenceRequest(
                parameters=Parameters(content_type="np"),
                inputs=[
                    RequestInput(
                        name="bar",
                        shape=[2],
                        data=[1, 2],
                        datatype="FP32",
                    )
                ],
            ),
            np.array([1, 2], dtype=float),
            StringCodec,
        ),
        # Request with a content type at the input level
        (
            InferenceRequest(
                inputs=[
                    RequestInput(
                        name="bar",
                        shape=[1, 3],
                        data=b"abc",
                        datatype="BYTES",
                        parameters=Parameters(content_type="str"),
                    )
                ],
            ),
            InferenceRequest(
                inputs=[
                    RequestInput(
                        name="bar",
                        shape=[1, 3],
                        data=b"abc",
                        datatype="BYTES",
                        parameters=Parameters(
                            content_type="str",
                        ),
                    )
                ],
            ),
            None,
        ),
        # Request combining content type annotations at both the input and
        # request levels
        (
            InferenceRequest(
                parameters=Parameters(content_type=PandasCodec.ContentType),
                inputs=[
                    RequestInput(name="a", datatype="INT64", shape=[3], data=[1, 2, 3]),
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
            None,
        ),
    ],
)
def test_decode_request(
    sum_model: MLModel,
    inference_request: InferenceRequest,
    expected: Any,
    default_codec: Optional[RequestCodec],
):
    decoded_request = sum_model.decode_request(inference_request, default_codec)

    if isinstance(expected, pd.DataFrame):
        pd.testing.assert_frame_equal(decoded_request, expected)  # type: ignore
    elif isinstance(expected, np.ndarray):
        np.testing.assert_array_equal(decoded_request, expected)  # type: ignore
    else:
        assert decoded_request == expected
