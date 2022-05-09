import pytest

from typing import Any

from mlserver.codecs import StringCodec
from mlserver.types import RequestInput, ResponseOutput, Parameters


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
def test_decode_input(request_input, expected):
    decoded = StringCodec.decode_input(request_input)

    assert decoded == expected


@pytest.mark.parametrize(
    "decoded, expected",
    [
        (
            ["hello world"],
            ResponseOutput(
                name="foo",
                shape=[1],
                datatype="BYTES",
                data=[b"hello world"],
                parameters=Parameters(content_type=StringCodec.ContentType),
            ),
        ),
        (
            ["hey", "whats"],
            ResponseOutput(
                name="foo",
                shape=[2],
                datatype="BYTES",
                data=[b"hey", b"whats"],
                parameters=Parameters(content_type=StringCodec.ContentType),
            ),
        ),
    ],
)
def test_encode_output(decoded, expected):
    response_output = StringCodec.encode_output(name="foo", payload=decoded)

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
def test_encode_input(decoded, expected):
    response_output = StringCodec.encode_output(name="foo", payload=decoded)
    request_input = StringCodec.encode_input(name="foo", payload=decoded)

    assert request_input.data.__root__ == response_output.data.__root__
    assert response_output.datatype == request_input.datatype
    assert request_input.parameters.content_type == StringCodec.ContentType
