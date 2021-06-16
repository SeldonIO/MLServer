import pytest

from mlserver.codecs import StringCodec
from mlserver.types import RequestInput


@pytest.mark.parametrize(
    "request_input, expected",
    [
        (
            RequestInput(name="foo", datatype="BYTES", shape=[], data=b"hello world"),
            ["hello world"],
        ),
        (
            RequestInput(name="foo", datatype="BYTES", shape=[], data="hello world"),
            ["hello world"],
        ),
        (
            RequestInput(name="foo", datatype="BYTES", shape=[], data=["hello world"]),
            ["hello world"],
        ),
        (
            RequestInput(name="foo", datatype="BYTES", shape=[], data=[b"hello world"]),
            ["hello world"],
        ),
        (
            RequestInput(
                name="foo", datatype="BYTES", shape=[1, 11], data=b"hello world"
            ),
            ["hello world"],
        ),
        (
            RequestInput(
                name="foo",
                datatype="BYTES",
                shape=[2, 11],
                data=["hello world", "hello world"],
            ),
            ["hello world", "hello world"],
        ),
        (
            RequestInput(name="foo", datatype="BYTES", shape=[2, 3], data=b"heyabc"),
            ["hey", "abc"],
        ),
    ],
)
def test_decode(request_input, expected):
    codec = StringCodec()
    decoded = codec.decode(request_input)

    assert decoded == expected


@pytest.mark.parametrize(
    "decoded, expected",
    [
        (
            ["hello world"],
            RequestInput(
                name="foo", shape=[1, 11], datatype="BYTES", data=b"hello world"
            ),
        ),
        (
            ["hey", "abc"],
            RequestInput(name="foo", shape=[2, 3], datatype="BYTES", data=b"heyabc"),
        ),
    ],
)
def test_encode(decoded, expected):
    codec = StringCodec()
    response_output = codec.encode(name="foo", payload=decoded)

    assert expected == response_output
