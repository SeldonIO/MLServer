import pytest

from mlserver.codecs import Base64Codec
from mlserver.types import RequestInput, ResponseOutput


@pytest.mark.parametrize(
    "decoded, expected",
    [
        (
            [b"Python is fun"],
            ResponseOutput(
                name="foo",
                shape=[1, 20],
                datatype="BYTES",
                data=b"UHl0aG9uIGlzIGZ1bg==",
            ),
        ),
        (
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
