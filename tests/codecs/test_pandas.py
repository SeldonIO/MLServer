import pytest
import pandas as pd
import numpy as np

from typing import Any

from mlserver.codecs.pandas import PandasCodec, _to_response_output
from mlserver.types import (
    InferenceRequest,
    InferenceResponse,
    RequestInput,
    Parameters,
    ResponseOutput,
)


@pytest.mark.parametrize(
    "payload, expected",
    [
        (pd.DataFrame({"a": [1, 2, 3], "b": ["A", "B", "C"]}), True),
        ({"a": [1, 2, 3]}, False),
    ],
)
def test_can_encode(payload: Any, expected: bool):
    assert PandasCodec.can_encode(payload) == expected


@pytest.mark.parametrize(
    "series, use_bytes, expected",
    [
        (
            pd.Series(data=["hey", "abc"], name="foo"),
            True,
            ResponseOutput(
                name="foo", shape=[2], data=[b"hey", b"abc"], datatype="BYTES"
            ),
        ),
        (
            pd.Series(data=["hey", "abc"], name="foo"),
            False,
            ResponseOutput(
                name="foo", shape=[2], data=["hey", "abc"], datatype="BYTES"
            ),
        ),
        (
            pd.Series(data=[1, 2, 3], name="bar"),
            True,
            ResponseOutput(name="bar", shape=[3], data=[1, 2, 3], datatype="INT64"),
        ),
        (
            pd.Series(data=[1, 2.5, 3], name="bar"),
            True,
            ResponseOutput(
                name="bar", shape=[3], data=[1.0, 2.5, 3.0], datatype="FP64"
            ),
        ),
        (
            pd.Series(data=[[1, 2, 3], [4, 5, 6]], name="bar"),
            True,
            ResponseOutput(
                name="bar", shape=[2], data=[[1, 2, 3], [4, 5, 6]], datatype="BYTES"
            ),
        ),
    ],
)
def test_to_response_output(series, use_bytes, expected):
    response_output = _to_response_output(series, use_bytes=use_bytes)

    assert response_output == expected


@pytest.mark.parametrize(
    "dataframe, use_bytes, expected",
    [
        (
            pd.DataFrame(
                {
                    "a": [1, 2, 3],
                    "b": ["A", "B", "C"],
                }
            ),
            True,
            InferenceResponse(
                model_name="my-model",
                outputs=[
                    ResponseOutput(
                        name="a", shape=[3], datatype="INT64", data=[1, 2, 3]
                    ),
                    ResponseOutput(
                        name="b", shape=[3], datatype="BYTES", data=[b"A", b"B", b"C"]
                    ),
                ],
            ),
        ),
        (
            pd.DataFrame(
                {
                    "a": [1, 2, 3],
                    "b": ["A", "B", "C"],
                }
            ),
            False,
            InferenceResponse(
                model_name="my-model",
                outputs=[
                    ResponseOutput(
                        name="a", shape=[3], datatype="INT64", data=[1, 2, 3]
                    ),
                    ResponseOutput(
                        name="b", shape=[3], datatype="BYTES", data=["A", "B", "C"]
                    ),
                ],
            ),
        ),
    ],
)
def test_encode_response(dataframe, use_bytes, expected):
    inference_response = PandasCodec.encode_response(
        expected.model_name,
        dataframe,
        model_version=expected.model_version,
        use_bytes=use_bytes,
    )

    assert inference_response == expected


@pytest.mark.parametrize(
    "response, expected",
    [
        (
            InferenceResponse(
                model_name="my-model",
                outputs=[
                    ResponseOutput(
                        name="a", shape=[3], datatype="INT64", data=[1, 2, 3]
                    ),
                    ResponseOutput(
                        name="b", shape=[3], datatype="BYTES", data=[b"A", b"B", b"C"]
                    ),
                ],
            ),
            pd.DataFrame(
                {
                    "a": [1, 2, 3],
                    "b": [b"A", b"B", b"C"],
                }
            ),
        ),
        (
            InferenceResponse(
                model_name="my-model",
                outputs=[
                    ResponseOutput(
                        name="a", shape=[3], datatype="INT64", data=[1, 2, 3]
                    ),
                    ResponseOutput(
                        name="b",
                        shape=[3],
                        datatype="BYTES",
                        data=[b"A", b"B", b"C"],
                        parameters=Parameters(_decoded_payload=["A", "B", "C"]),
                    ),
                ],
            ),
            pd.DataFrame(
                {
                    "a": [1, 2, 3],
                    "b": ["A", "B", "C"],
                }
            ),
        ),
    ],
)
def test_decode_response(response: InferenceResponse, expected: pd.DataFrame):
    decoded = PandasCodec.decode_response(response)
    pd.testing.assert_frame_equal(decoded, expected)


@pytest.mark.parametrize(
    "dataframe, use_bytes, expected",
    [
        (
            pd.DataFrame(
                {
                    "a": [1, 2, 3],
                    "b": ["A", "B", "C"],
                }
            ),
            True,
            InferenceRequest(
                inputs=[
                    RequestInput(name="a", shape=[3], datatype="INT64", data=[1, 2, 3]),
                    RequestInput(
                        name="b", shape=[3], datatype="BYTES", data=[b"A", b"B", b"C"]
                    ),
                ],
            ),
        ),
        (
            pd.DataFrame(
                {
                    "a": [1, 2, 3],
                    "b": ["A", "B", "C"],
                }
            ),
            False,
            InferenceRequest(
                inputs=[
                    RequestInput(name="a", shape=[3], datatype="INT64", data=[1, 2, 3]),
                    RequestInput(
                        name="b", shape=[3], datatype="BYTES", data=["A", "B", "C"]
                    ),
                ],
            ),
        ),
    ],
)
def test_encode_request(
    dataframe: pd.DataFrame, use_bytes: bool, expected: InferenceRequest
):
    inference_request = PandasCodec.encode_request(dataframe, use_bytes=use_bytes)
    assert inference_request == expected


@pytest.mark.parametrize(
    "inference_request, expected",
    [
        (
            InferenceRequest(
                inputs=[
                    RequestInput(
                        name="a",
                        data=[1, 2, 3],
                        datatype="FP32",
                        shape=[1, 3],
                        parameters=Parameters(_decoded_payload=np.array([[1, 2, 3]])),
                    ),
                    RequestInput(
                        name="b",
                        data=b"hello world",
                        datatype="BYTES",
                        shape=[1],
                        parameters=Parameters(_decoded_payload=["hello world"]),
                    ),
                ]
            ),
            pd.DataFrame({"a": [np.array([1, 2, 3])], "b": ["hello world"]}),
        ),
        (
            InferenceRequest(
                inputs=[
                    RequestInput(
                        name="a",
                        data=[1, 2, 3],
                        datatype="FP32",
                        shape=[3, 1],
                        parameters=Parameters(
                            _decoded_payload=np.array([[1], [2], [3]])
                        ),
                    ),
                    RequestInput(
                        name="b",
                        data=b"ABC",
                        datatype="BYTES",
                        shape=[3],
                    ),
                ]
            ),
            pd.DataFrame(
                {
                    "a": [[1], [2], [3]],
                    "b": [a for a in b"ABC"],
                }
            ),
        ),
        (
            InferenceRequest(
                inputs=[
                    RequestInput(
                        name="a",
                        data=[1],
                        datatype="INT32",
                        shape=[1],
                        parameters=Parameters(_decoded_payload=np.array([1])),
                    ),
                ]
            ),
            pd.DataFrame({"a": np.array([1], dtype=np.int32)}),
        ),
    ],
)
def test_decode_request(inference_request, expected):
    decoded = PandasCodec.decode_request(inference_request)

    pd.testing.assert_frame_equal(decoded, expected)
