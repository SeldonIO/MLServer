import pytest
import numpy as np


from mlserver.codecs.pack import pack_bytes, pack_tensor, unpack_bytes, unpack_tensor
from mlserver.codecs.numpy import NumpyCodec


def test_unpack_bytes():
    raw = b"\x03\x00\x00\x00one\x03\x00\x00\x00two\x05\x00\x00\x00three"
    expected = [b"one", b"two", b"three"]

    unpacked = unpack_bytes(raw)
    assert unpacked == expected


def test_pack_bytes():
    unpacked = [b"one", b"two", b"three"]
    expected = b"\x03\x00\x00\x00one\x03\x00\x00\x00two\x05\x00\x00\x00three"

    packed = pack_bytes(unpacked)
    assert packed == expected


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

    unpacked = unpack_tensor(request_input, raw)
    request_input.data = unpacked
    decoded = NumpyCodec.decode_input(request_input)

    np.testing.assert_allclose(decoded, tensor)


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
def test_pack_tensor(tensor: np.ndarray):
    request_input = NumpyCodec.encode_input(name="foo", payload=tensor)
    packed = pack_tensor(request_input)

    expected = tensor.tobytes()

    assert expected == packed
