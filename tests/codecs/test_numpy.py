import pytest
import numpy as np

from mlserver.codecs.numpy import NumpyCodec, _to_datatype
from mlserver.types import RequestInput


@pytest.mark.parametrize(
    "request_input, payload",
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
            RequestInput(name="foo", shape=[2, 1], data=b"\x01\x02", datatype="BYTES"),
            np.array([[b"\x01"], [b"\x02"]], dtype=bytes),
        ),
    ],
)
def test_numpy_codec(request_input, payload):
    codec = NumpyCodec()
    decoded = codec.decode(request_input)

    np.testing.assert_array_equal(decoded, payload)

    response_output = codec.encode(name="foo", payload=decoded)

    assert response_output.datatype == request_input.datatype
    assert response_output.shape == request_input.shape
    assert response_output.data == request_input.data


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
    ],
)
def test_to_datatype(dtype, datatype):
    dtype = np.dtype(dtype)

    obtained_datatype = _to_datatype(dtype)
    assert datatype == obtained_datatype
