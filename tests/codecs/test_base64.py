import pytest

from typing import Any

from mlserver.codecs import Base64Codec
from mlserver.types import RequestInput, ResponseOutput


@pytest.mark.parametrize(
    "payload, expected",
    [
        ([b"Python is fun", b"foo"], True),
        ([b"Python is fun", "foo"], False),
        (b"Python is fun", False),
        ("foo", False),
    ],
)
def test_can_encode(payload: Any, expected: bool):
    assert Base64Codec.can_encode(payload) == expected


@pytest.mark.parametrize(
    "decoded, expected",
    [
        (
            # List with a single binary string
            [b"Python is fun"],
            ResponseOutput(
                name="foo",
                shape=[1],
                datatype="BYTES",
                data=[b"UHl0aG9uIGlzIGZ1bg=="],
            ),
        ),
        (
            # List with a single (non-binary) string
            ["Python is fun"],
            ResponseOutput(
                name="foo",
                shape=[1],
                datatype="BYTES",
                data=[b"UHl0aG9uIGlzIGZ1bg=="],
            ),
        ),
        (
            # List with two binary strings
            [b"Python is fun", b"Python is fun"],
            ResponseOutput(
                name="foo",
                shape=[2],
                datatype="BYTES",
                data=[b"UHl0aG9uIGlzIGZ1bg==", b"UHl0aG9uIGlzIGZ1bg=="],
            ),
        ),
    ],
)
def test_encode(decoded, expected):
    codec = Base64Codec()
    response_output = codec.encode(name="foo", payload=decoded)

    assert expected == response_output


@pytest.mark.parametrize(
    "encoded, expected",
    [
        (
            # Single base64-encoded binary string
            RequestInput(
                name="foo",
                shape=[1],
                datatype="BYTES",
                data="UHl0aG9uIGlzIGZ1bg==",
            ),
            [b"Python is fun"],
        ),
        (
            # Single (non-base64-encoded) binary string
            RequestInput(
                name="foo",
                shape=[1],
                datatype="BYTES",
                data=b"Python is fun",
            ),
            [b"Python is fun"],
        ),
        (
            # Single (non-base64-encoded) (non-binary) string
            RequestInput(
                name="foo",
                shape=[1],
                datatype="BYTES",
                data="Python is fun",
            ),
            [b"Python is fun"],
        ),
        (
            # Multiple base64-encoded binary strings
            RequestInput(
                name="foo",
                shape=[2],
                datatype="BYTES",
                data=[b"UHl0aG9uIGlzIGZ1bg==", b"UHl0aG9uIGlzIGZ1bg=="],
            ),
            [b"Python is fun", b"Python is fun"],
        ),
    ],
)
def test_decode(encoded, expected):
    codec = Base64Codec()
    decoded_input = codec.decode(encoded)

    assert expected == decoded_input
