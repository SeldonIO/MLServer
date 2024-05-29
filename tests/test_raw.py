import pytest
import numpy as np

from typing import List

from mlserver.types import RequestInput, ResponseOutput, TensorData
from mlserver.raw import (
    _pack_bytes,
    _pack_tensor,
    _unpack_bytes,
    _unpack_tensor,
    extract_raw,
    inject_raw,
)
from mlserver.codecs.numpy import NumpyCodec


def test_unpack_bytes():
    raw = b"\x03\x00\x00\x00one\x03\x00\x00\x00two\x05\x00\x00\x00three"
    expected = [b"one", b"two", b"three"]

    unpacked = _unpack_bytes(raw)
    assert unpacked == expected


@pytest.mark.parametrize(
    "unpacked",
    [
        [b"one", b"two", b"three"],
        ["one", "two", "three"],
    ],
)
def test_pack_bytes(unpacked: List[str]):
    expected = b"\x03\x00\x00\x00one\x03\x00\x00\x00two\x05\x00\x00\x00three"

    packed = _pack_bytes(unpacked)
    assert packed == expected


@pytest.mark.parametrize(
    "tensor",
    [
        # bool
        np.array([[True, False, True]]),
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
    packed = _pack_tensor(request_input)

    expected = tensor.tobytes()

    assert expected == packed


@pytest.mark.parametrize(
    "inputs, raw_contents, expected",
    [
        # With only raw entries
        (
            [
                RequestInput(name="foo", datatype="BYTES", shape=[3], data=[]),
                RequestInput(name="bar", datatype="FP32", shape=[3, 2], data=[]),
            ],
            [
                b"\x03\x00\x00\x00one\x03\x00\x00\x00two\x05\x00\x00\x00three",
                np.array([1, 2, 3, 4, 5, 6], dtype=np.single).tobytes(),
            ],
            [
                TensorData([b"one", b"two", b"three"]),
                TensorData([1, 2, 3, 4, 5, 6]),
            ],
        ),
        # With mixed entries (i.e. raw and normal)
        (
            [
                RequestInput(name="foo", datatype="BYTES", shape=[3], data=[]),
                RequestInput(
                    name="bar", datatype="FP32", shape=[3, 2], data=[1, 2, 3, 4, 5, 6]
                ),
                RequestInput(name="foo2", datatype="FP32", shape=[2, 2], data=[]),
            ],
            [
                b"\x03\x00\x00\x00one\x03\x00\x00\x00two\x05\x00\x00\x00three",
                np.array([7, 8, 9, 10], dtype=np.single).tobytes(),
            ],
            [
                TensorData([b"one", b"two", b"three"]),
                TensorData([1, 2, 3, 4, 5, 6]),
                TensorData([7, 8, 9, 10]),
            ],
        ),
    ],
)
def test_inject_raw(
    inputs: List[RequestInput], raw_contents: List[bytes], expected: list
):
    with_unpacked_raw = inject_raw(inputs, raw_contents)

    assert len(with_unpacked_raw) == len(expected)
    for request_input, expected in zip(with_unpacked_raw, expected):
        assert request_input.data == expected


def test_extract_raw():
    inputs = [
        ResponseOutput(
            name="foo", datatype="BYTES", shape=[3], data=[b"one", b"two", b"three"]
        ),
        ResponseOutput(
            name="bar", datatype="FP32", shape=[3, 2], data=[1, 2, 3, 4, 5, 6]
        ),
    ]

    expected = [
        b"\x03\x00\x00\x00one\x03\x00\x00\x00two\x05\x00\x00\x00three",
        np.array([1, 2, 3, 4, 5, 6], dtype=np.single).tobytes(),
    ]

    without_data, raw_contents = extract_raw(inputs)

    assert raw_contents == expected
    assert len(expected) == len(without_data)
    for response_output in without_data:
        assert len(response_output.data) == 0
