import pytest
import numpy as np

from typing import List

from mlserver.types import RequestInput
from mlserver.codecs.raw import RawInputCodec, _unpack_tensor
from mlserver.codecs.numpy import NumpyCodec


@pytest.mark.parametrize(
    "tensor",
    [
        # bool
        np.array([True, False, True]),
        # uint8
        np.array([[1, 2], [3, 4]], dtype=np.ubyte),
        # uint16
        np.array([[1, 2], [3, 4]], dtype=np.ushort),
        # uint32
        np.array([[1, 2], [3, 4]], dtype=np.uintc),
        # uint64
        np.array([[1, 2], [3, 4]], dtype=np.uint),
        # int8
        np.array([[1], [-2], [3]], dtype=np.byte),
        # int16
        np.array([[1], [-2], [3]], dtype=np.short),
        # int32
        np.array([[1], [-2], [3]], dtype=np.intc),
        # int64
        np.array([[1], [-2], [3]], dtype=np.int_),
        # fp16
        np.array([[1.2, 3.3]], dtype=np.half),
        # fp32
        np.array([[1.2, 3.3]], dtype=np.single),
        # fp64
        np.array([[1.2, 3.3]], dtype=np.double),
    ],
)
def test_unpack_tensor(tensor: np.ndarray):
    request_input = NumpyCodec.encode_input(name="foo", payload=tensor)
    request_input.data = []
    raw = tensor.tobytes()

    unpacked = _unpack_tensor(request_input, raw)
    request_input.data = unpacked
    decoded = NumpyCodec.decode_input(request_input)

    np.testing.assert_allclose(decoded, tensor)


@pytest.mark.parametrize(
    "request_input, raw, expected",
    [
        (
            RequestInput(name="foo", datatype="BYTES", shape=[3], data=[]),
            b"\x03\x00\x00\x00one\x03\x00\x00\x00two\x05\x00\x00\x00three",
            [b"one", b"two", b"three"],
        ),
        (
            RequestInput(
                name="foo", datatype="FP32", shape=[3, 2], data=[1, 2, 3, 4, 5, 6]
            ),
            np.array([1, 2, 3, 4, 5, 6], dtype=np.single).tobytes(),
            [1, 2, 3, 4, 5, 6],
        ),
    ],
)
def test_decode_input(request_input: RequestInput, raw: bytes, expected: list):
    decoded_input = RawInputCodec.decode_input(request_input, raw=raw)
    assert decoded_input.data == expected
