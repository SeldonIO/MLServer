import pytest

from typing import Any

from mlserver.codecs import StringCodec
from mlserver.types import RequestInput, ResponseOutput


@pytest.mark.parametrize(
    "payload, expected",
    [
        (["foo", "foo2"], True),
        (["foo", b"foo2"], False),
        ("foo", False),
        (b"foo", False),
    ],
)
def test_can_encode(payload: Any, expected: bool):
    assert StringCodec.can_encode(payload) == expected


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
            RequestInput(name="foo", datatype="BYTES", shape=[1], data=b"hello world"),
            ["hello world"],
        ),
        (
            RequestInput(
                name="foo",
                datatype="BYTES",
                shape=[2],
                data=["hello world", "hello world"],
            ),
            ["hello world", "hello world"],
        ),
        (
            RequestInput(
                name="foo", datatype="BYTES", shape=[2], data=[b"hey", b"whats"]
            ),
            ["hey", "whats"],
        ),
        (
            RequestInput(name="foo", datatype="BYTES", shape=[2], data=[None]),
            [None],
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
            ResponseOutput(
                name="foo", shape=[1], datatype="BYTES", data=[b"hello world"]
            ),
        ),
        (
            ["hey", "whats"],
            ResponseOutput(
                name="foo", shape=[2], datatype="BYTES", data=[b"hey", b"whats"]
            ),
        ),
    ],
)
def test_encode(decoded, expected):
    codec = StringCodec()
    response_output = codec.encode(name="foo", payload=decoded)

    assert expected == response_output


@pytest.mark.parametrize(
    "decoded, expected",
    [
        (
            ["hello world"],
            ResponseOutput(
                name="foo", shape=[1], datatype="BYTES", data=[b"hello world"]
            ),
        ),
        (
            ["hey", "whats"],
            ResponseOutput(
                name="foo", shape=[2], datatype="BYTES", data=[b"hey", b"whats"]
            ),
        ),
    ],
)
def test_encode_request_input(decoded, expected):
    # we only support variable length string to be transferred over REST
    codec = StringCodec()
    response_output = codec.encode(name="foo", payload=decoded)

    request_input = codec.encode_request_input(name="foo", payload=decoded)
    assert request_input.data.__root__ == decoded
    assert response_output.datatype == request_input.datatype
    assert request_input.parameters.content_type == codec.ContentType
