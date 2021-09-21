import pytest

from mlserver.codecs import Base64Codec
from mlserver.types import RequestInput, ResponseOutput


@pytest.mark.parametrize(
    "decoded, expected",
    [
        (
            # List with a single binary string
            [b"Python is fun"],
            ResponseOutput(
                name="foo",
                shape=[1, 20],
                datatype="BYTES",
                data=b"UHl0aG9uIGlzIGZ1bg==",
            ),
        ),
        (
            # List with a single (non-binary) string
            ["Python is fun"],
            ResponseOutput(
                name="foo",
                shape=[1, 20],
                datatype="BYTES",
                data=b"UHl0aG9uIGlzIGZ1bg==",
            ),
        ),
        (
            # List with two binary strings
            [b"Python is fun", b"Python is fun"],
            ResponseOutput(
                name="foo",
                shape=[2, 20],
                datatype="BYTES",
                data=b"UHl0aG9uIGlzIGZ1bg==UHl0aG9uIGlzIGZ1bg==",
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
                shape=[1, 20],
                datatype="BYTES",
                data="UHl0aG9uIGlzIGZ1bg==",
            ),
            [b"Python is fun"],
        ),
        (
            # Single (non-base64-encoded) binary string
            RequestInput(
                name="foo",
                shape=[1, 13],
                datatype="BYTES",
                data=b"Python is fun",
            ),
            [b"Python is fun"],
        ),
        (
            # Single (non-base64-encoded) (non-binary) string
            RequestInput(
                name="foo",
                shape=[1, 13],
                datatype="BYTES",
                data="Python is fun",
            ),
            [b"Python is fun"],
        ),
        (
            # Multiple base64-encoded binary strings
            RequestInput(
                name="foo",
                shape=[2, 20],
                datatype="BYTES",
                data=b"UHl0aG9uIGlzIGZ1bg==UHl0aG9uIGlzIGZ1bg==",
            ),
            [b"Python is fun", b"Python is fun"],
        ),
    ],
)
def test_decode(encoded, expected):
    codec = Base64Codec()
    decoded_input = codec.decode(encoded)

    assert expected == decoded_input
