import pytest
import numpy as np

from typing import Any

from mlserver.types import RequestInput, Parameters, TensorData
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
            TensorData(__root__=[1, 2]),
        ),
        (
            RequestInput(
                name="bar",
                shape=[2],
                data=[1, 2],
                datatype="FP32",
            ),
            TensorData(__root__=[1, 2]),
        ),
    ],
)
def test_decode(sum_model: MLModel, request_input: RequestInput, expected: Any):
    decoded = sum_model.decode(request_input)

    if isinstance(expected, np.ndarray):
        np.testing.assert_array_equal(decoded, expected)  # type: ignore
    else:
        assert decoded == expected  # type: ignore
