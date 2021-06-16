import pytest
import pandas as pd
import numpy as np

from mlserver.codecs.pandas import PandasCodec, _to_response_output
from mlserver.types import (
    InferenceRequest,
    InferenceResponse,
    RequestInput,
    Parameters,
    ResponseOutput,
)


@pytest.mark.parametrize(
    "series, expected",
    [
        (
            pd.Series(data=["hey", "abc"], name="foo"),
            ResponseOutput(
                name="foo", shape=[2], data=["hey", "abc"], datatype="BYTES"
            ),
        ),
        (
            pd.Series(data=[1, 2, 3], name="bar"),
            ResponseOutput(name="bar", shape=[3], data=[1, 2, 3], datatype="INT64"),
        ),
        (
            pd.Series(data=[1, 2.5, 3], name="bar"),
            ResponseOutput(
                name="bar", shape=[3], data=[1.0, 2.5, 3.0], datatype="FP64"
            ),
        ),
        (
            pd.Series(data=[[1, 2, 3], [4, 5, 6]], name="bar"),
            ResponseOutput(
                name="bar", shape=[2], data=[[1, 2, 3], [4, 5, 6]], datatype="BYTES"
            ),
        ),
    ],
)
def test_to_response_output(series, expected):
    response_output = _to_response_output(series)

    assert response_output == expected


@pytest.mark.parametrize(
    "dataframe, expected",
    [
        (
            pd.DataFrame(
                {
                    "a": [1, 2, 3],
                    "b": ["A", "B", "C"],
                }
            ),
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
        )
    ],
)
def test_encode(dataframe, expected):
    codec = PandasCodec()
    inference_response = codec.encode(
        expected.model_name, dataframe, model_version=expected.model_version
    )

    assert inference_response == expected


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
                        shape=[1, 11],
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
                        shape=[3, 1],
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
    ],
)
def test_decode(inference_request, expected):
    codec = PandasCodec()
    decoded = codec.decode(inference_request)

    pd.testing.assert_frame_equal(decoded, expected)
