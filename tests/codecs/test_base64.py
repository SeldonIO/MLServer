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
def test_encode_output(decoded, expected):
    response_output = Base64Codec.encode_output(name="foo", payload=decoded)

    assert expected == response_output


@pytest.mark.parametrize(
    "encoded, expected",
    [
        (
            # Single base64-encoded binary string
            ResponseOutput(
                name="foo",
                shape=[1],
                datatype="BYTES",
                data="UHl0aG9uIGlzIGZ1bg==",
            ),
            [b"Python is fun"],
        ),
        (
            # Single (non-base64-encoded) binary string
            ResponseOutput(
                name="foo",
                shape=[1],
                datatype="BYTES",
                data=b"Python is fun",
            ),
            [b"Python is fun"],
        ),
        (
            # Single (non-base64-encoded) (non-binary) string
            ResponseOutput(
                name="foo",
                shape=[1],
                datatype="BYTES",
                data="Python is fun",
            ),
            [b"Python is fun"],
        ),
        (
            # Multiple base64-encoded binary strings
            ResponseOutput(
                name="foo",
                shape=[2],
                datatype="BYTES",
                data=[b"UHl0aG9uIGlzIGZ1bg==", b"UHl0aG9uIGlzIGZ1bg=="],
            ),
            [b"Python is fun", b"Python is fun"],
        ),
    ],
)
def test_decode_output(encoded, expected):
    decoded_output = Base64Codec.decode_output(encoded)

    assert expected == decoded_output


@pytest.mark.parametrize(
    "decoded, expected",
    [
        (
            # List with a single binary string
            [b"Python is fun"],
            RequestInput(
                name="foo",
                shape=[1],
                datatype="BYTES",
                data=[b"UHl0aG9uIGlzIGZ1bg=="],
            ),
        ),
        (
            # List with a single (non-binary) string
            ["Python is fun"],
            RequestInput(
                name="foo",
                shape=[1],
                datatype="BYTES",
                data=[b"UHl0aG9uIGlzIGZ1bg=="],
            ),
        ),
        (
            # List with two binary strings
            [b"Python is fun", b"Python is fun"],
            RequestInput(
                name="foo",
                shape=[2],
                datatype="BYTES",
                data=[b"UHl0aG9uIGlzIGZ1bg==", b"UHl0aG9uIGlzIGZ1bg=="],
            ),
        ),
    ],
)
def test_encode_input(decoded, expected):
    request_input = Base64Codec.encode_input(name="foo", payload=decoded)

    assert expected == request_input


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
def test_decode_input(encoded, expected):
    decoded_input = Base64Codec.decode_input(encoded)

    assert expected == decoded_input
