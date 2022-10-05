import pytest
import numpy as np

from mlserver.types import RequestInput
from mlserver.codecs.raw import RawInputCodec


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
def test_encode_input(request_input: RequestInput, raw: bytes, expected: list):
    encoded_input = RawInputCodec.encode_input(request_input, raw=raw)
    assert encoded_input.data == expected
