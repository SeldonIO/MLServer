import pytest
import numpy as np

from typing import Any

from mlserver.types import RequestInput, Parameters
from mlserver.codecs import NumpyCodec, StringCodec
from mlserver.model import MLModel


@pytest.mark.parametrize(
    "request_input,expected",
    [
        (
            RequestInput(
                name="foo",
                shape=[2, 2],
                data=[1, 2, 3, 4],
                datatype="INT32",
                parameters=Parameters(content_type=NumpyCodec.ContentType),
            ),
            np.array([[1, 2], [3, 4]]),
        ),
        (
            RequestInput(
                name="bar",
                shape=[2],
                data=[1, 2],
                datatype="FP32",
                parameters=Parameters(content_type=NumpyCodec.ContentType),
            ),
            np.array([1, 2], dtype=np.float32),
        ),
        (
            RequestInput(
                name="bar",
                shape=[2],
                data=[1, 2],
                datatype="FP32",
            ),
            None,
        ),
        (
            RequestInput(
                name="foo",
                shape=[17],
                data=b"my unicode string",
                datatype="BYTES",
                parameters=Parameters(content_type=StringCodec.ContentType),
            ),
            "my unicode string",
        ),
        (
            # sum-model has metadata setting the default content type of input
            # `input-0` to `np`
            RequestInput(
                name="input-0",
                shape=[2, 2],
                data=[1, 2, 3, 4],
                datatype="INT32",
            ),
            np.array([[1, 2], [3, 4]]),
        ),
    ],
)
def test_decode(sum_model: MLModel, request_input: RequestInput, expected: Any):
    decoded = sum_model.decode(request_input)

    if expected is None:
        # No decoder was found
        assert decoded == request_input.data
    elif isinstance(expected, np.ndarray):
        np.testing.assert_array_equal(decoded, expected)  # type: ignore
    else:
        assert decoded == expected  # type: ignore
