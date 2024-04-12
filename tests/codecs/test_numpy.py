import pytest
import numpy as np

from typing import Any

from mlserver.codecs.numpy import NumpyCodec, to_datatype
from mlserver.types import RequestInput, ResponseOutput, Parameters, Datatype


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
            ResponseOutput(
                name="foo",
                shape=[3, 1],
                data=[1, 2, 3],
                datatype="INT64",
                parameters=Parameters(content_type=NumpyCodec.ContentType),
            ),
        ),
        (
            np.array([[1, 2], [3, 4]]),
            ResponseOutput(
                name="foo",
                shape=[2, 2],
                data=[1, 2, 3, 4],
                datatype="INT64",
                parameters=Parameters(content_type=NumpyCodec.ContentType),
            ),
        ),
        (
            np.array([[1, 2], [3, 4]], dtype=np.int32),
            ResponseOutput(
                name="foo",
                shape=[2, 2],
                data=[1, 2, 3, 4],
                datatype="INT32",
                parameters=Parameters(content_type=NumpyCodec.ContentType),
            ),
        ),
        (
            np.array([1.0, 2.0]),
            ResponseOutput(
                name="foo",
                shape=[2, 1],
                data=[1, 2],
                datatype="FP64",
                parameters=Parameters(content_type=NumpyCodec.ContentType),
            ),
        ),
        (
            np.array([[b"\x01"], [b"\x02"]], dtype=bytes),
            ResponseOutput(
                name="foo",
                shape=[2, 1],
                data=[b"\x01\x02"],
                datatype="BYTES",
                parameters=Parameters(content_type=NumpyCodec.ContentType),
            ),
        ),
        (
            np.array(["foo", "bar"], dtype=str),
            ResponseOutput(
                name="foo",
                shape=[2, 1],
                data=[b"foo", b"bar"],
                datatype="BYTES",
                parameters=Parameters(content_type=NumpyCodec.ContentType),
            ),
        ),
        (
            np.array([None, "bar"]),
            ResponseOutput(
                name="foo",
                shape=[2, 1],
                data=[None, "bar"],
                datatype="BYTES",
                parameters=Parameters(content_type=NumpyCodec.ContentType),
            ),
        ),
        (
            np.array([2.3, 3.4, np.NaN]),
            ResponseOutput(
                name="foo",
                shape=[3, 1],
                data=[2.3, 3.4, None],
                datatype="FP64",
                parameters=Parameters(content_type=NumpyCodec.ContentType),
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
        (
            RequestInput(name="foo", shape=[3], data=[1, 2, None], datatype="FP16"),
            np.array([1, 2, np.NaN], dtype="float16"),
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
def test_codec_idempotent(request_input: RequestInput):
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
        (np.bool_, Datatype.BOOL),
        (np.uint8, Datatype.UINT8),
        (np.uint16, Datatype.UINT16),
        (np.uint32, Datatype.UINT32),
        (np.uint64, Datatype.UINT64),
        (np.int8, Datatype.INT8),
        (np.int16, Datatype.INT16),
        (np.int32, Datatype.INT32),
        (np.int64, Datatype.INT64),
        (np.float16, Datatype.FP16),
        (np.float32, Datatype.FP32),
        (np.float64, Datatype.FP64),
        (np.byte, Datatype.INT8),
        (bytes, Datatype.BYTES),
        (str, Datatype.BYTES),
    ],
)
def test_to_datatype(dtype, datatype):
    dtype = np.dtype(dtype)

    obtained_datatype = to_datatype(dtype)
    assert datatype == obtained_datatype
