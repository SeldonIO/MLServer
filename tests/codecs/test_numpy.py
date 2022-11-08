import pytest
import numpy as np

from typing import Any

from mlserver.codecs.numpy import NumpyCodec, to_datatype
from mlserver.types import RequestInput, ResponseOutput


@pytest.mark.parametrize(
    "payload, expected",
    [(np.array([1, 2, 3]), True), (np.array(["foo", "bar"]), True), ([1, 2, 3], False)],
)
def test_can_encode(payload: Any, expected: bool):
    assert NumpyCodec.can_encode(payload) == expected


@pytest.mark.parametrize(
    "payload, expected",
    [
        (
            np.array([1, 2, 3]),
            ResponseOutput(name="foo", shape=[3, 1], data=[1, 2, 3], datatype="INT64"),
        ),
        (
            np.array([[1, 2], [3, 4]]),
            ResponseOutput(
                name="foo", shape=[2, 2], data=[1, 2, 3, 4], datatype="INT64"
            ),
        ),
        (
            np.array([[1, 2], [3, 4]], dtype=np.int32),
            ResponseOutput(
                name="foo", shape=[2, 2], data=[1, 2, 3, 4], datatype="INT32"
            ),
        ),
        (
            np.array([1.0, 2.0]),
            ResponseOutput(name="foo", shape=[2, 1], data=[1, 2], datatype="FP64"),
        ),
        (
            np.array([[b"\x01"], [b"\x02"]], dtype=bytes),
            ResponseOutput(
                name="foo", shape=[2, 1], data=[b"\x01\x02"], datatype="BYTES"
            ),
        ),
        (
            np.array(["foo", "bar"], dtype=str),
            ResponseOutput(
                name="foo", shape=[2, 1], data=[b"foo", b"bar"], datatype="BYTES"
            ),
        ),
    ],
)
def test_encode_output(payload: np.ndarray, expected: ResponseOutput):
    response_output = NumpyCodec.encode_output(name="foo", payload=payload)
    assert response_output == expected


@pytest.mark.parametrize(
    "request_input, expected",
    [
        (
            RequestInput(name="foo", shape=[3], data=[1, 2, 3], datatype="INT32"),
            np.array([1, 2, 3]),
        ),
        (
            RequestInput(name="foo", shape=[2, 2], data=[1, 2, 3, 4], datatype="INT32"),
            np.array([[1, 2], [3, 4]]),
        ),
        (
            RequestInput(name="foo", shape=[2], data=[1, 2], datatype="FP32"),
            np.array([1.0, 2.0]),
        ),
        (
            RequestInput(
                name="foo", shape=[2, 1], data=[b"\x01", b"\x02"], datatype="BYTES"
            ),
            np.array([[b"\x01"], [b"\x02"]], dtype=bytes),
        ),
        (
            RequestInput(name="foo", shape=[2], data=["foo", "bar"], datatype="BYTES"),
            np.array(["foo", "bar"], dtype=str),
        ),
    ],
)
def test_decode_input(request_input: RequestInput, expected: np.ndarray):
    decoded = NumpyCodec.decode_input(request_input)
    np.testing.assert_array_equal(decoded, expected)


@pytest.mark.parametrize(
    "request_input",
    [
        RequestInput(name="foo", shape=[3], data=[1, 2, 3], datatype="INT32"),
        RequestInput(name="foo", shape=[2, 2], data=[1, 2, 3, 4], datatype="INT32"),
        RequestInput(name="foo", shape=[2], data=[1, 2], datatype="FP32"),
        RequestInput(name="foo", shape=[2, 1], data=[b"\x01\x02"], datatype="BYTES"),
        RequestInput(name="foo", shape=[2], data=["foo", "bar"], datatype="BYTES"),
    ],
)
def test_encode_input(request_input):
    decoded = NumpyCodec.decode_input(request_input)
    response_output = NumpyCodec.encode_output(name="foo", payload=decoded)

    request_input_result = NumpyCodec.encode_input(name="foo", payload=decoded)
    assert response_output.datatype == request_input_result.datatype
    assert response_output.shape == request_input_result.shape
    assert response_output.data == request_input_result.data
    assert request_input_result.parameters.content_type == NumpyCodec.ContentType


@pytest.mark.parametrize(
    "payload, expected",
    [
        (np.array([1, 2, 3]), np.array([[1], [2], [3]])),
        (np.array([[1, 2], [3, 4]]), np.array([[1, 2], [3, 4]])),
        (np.array([1.0, 2.0]), np.array([[1.0], [2.0]])),
        (
            np.array([[b"\x01"], [b"\x02"]], dtype=bytes),
            np.array([[b"\x01"], [b"\x02"]], dtype=bytes),
        ),
    ],
)
def test_decode_output(payload, expected):
    # Note that `decode(encode(x)) != x`, because of shape changes to make
    # the `[N] == [N, 1]` explicit
    response_output = NumpyCodec.encode_output(name="foo", payload=payload)
    output_response_decoded = NumpyCodec.decode_output(response_output)
    np.testing.assert_array_equal(output_response_decoded, expected)


@pytest.mark.parametrize(
    "dtype, datatype",
    [
        (np.bool_, "BOOL"),
        (np.uint8, "UINT8"),
        (np.uint16, "UINT16"),
        (np.uint32, "UINT32"),
        (np.uint64, "UINT64"),
        (np.int8, "INT8"),
        (np.int16, "INT16"),
        (np.int32, "INT32"),
        (np.int64, "INT64"),
        (np.float16, "FP16"),
        (np.float32, "FP32"),
        (np.float64, "FP64"),
        (np.byte, "INT8"),
        (bytes, "BYTES"),
        (str, "BYTES"),
    ],
)
def test_to_datatype(dtype, datatype):
    dtype = np.dtype(dtype)

    obtained_datatype = to_datatype(dtype)
    assert datatype == obtained_datatype
