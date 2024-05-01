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
            RequestInput(
                name="foo", datatype="BYTES", shape=[1, 1], data=b"hello world"
            ),
            ["hello world"],
        ),
        (
            RequestInput(
                name="foo", datatype="BYTES", shape=[1, 1], data="hello world"
            ),
            ["hello world"],
        ),
        (
            RequestInput(
                name="foo", datatype="BYTES", shape=[1, 1], data=["hello world"]
            ),
            ["hello world"],
        ),
        (
            RequestInput(
                name="foo", datatype="BYTES", shape=[1, 1], data=[b"hello world"]
            ),
            ["hello world"],
        ),
        (
            RequestInput(
                name="foo", datatype="BYTES", shape=[1, 1], data=b"hello world"
            ),
            ["hello world"],
        ),
        (
            RequestInput(
                name="foo",
                datatype="BYTES",
                shape=[2, 1],
                data=["hello world", "hello world"],
            ),
            ["hello world", "hello world"],
        ),
        (
            RequestInput(
                name="foo", datatype="BYTES", shape=[2, 1], data=[b"hey", b"whats"]
            ),
            ["hey", "whats"],
        ),
        (
            RequestInput(name="foo", datatype="BYTES", shape=[1, 1], data=[None]),
            [None],
        ),
    ],
)
def test_decode_input(request_input, expected):
    decoded = StringCodec.decode_input(request_input)

    assert decoded == expected


@pytest.mark.parametrize(
    "decoded, use_bytes, expected",
    [
        (
            ["hello world"],
            True,
            ResponseOutput(
                name="foo",
                shape=[1, 1],
                datatype="BYTES",
                data=[b"hello world"],
                parameters=Parameters(content_type=StringCodec.ContentType),
            ),
        ),
        (
            ["hey", "whats"],
            True,
            ResponseOutput(
                name="foo",
                shape=[2, 1],
                datatype="BYTES",
                data=[b"hey", b"whats"],
                parameters=Parameters(content_type=StringCodec.ContentType),
            ),
        ),
        (
            ["hey", "whats"],
            False,
            ResponseOutput(
                name="foo",
                shape=[2, 1],
                datatype="BYTES",
                data=["hey", "whats"],
                parameters=Parameters(content_type=StringCodec.ContentType),
            ),
        ),
    ],
)
def test_encode_output(decoded, use_bytes, expected):
    response_output = StringCodec.encode_output(
        name="foo", payload=decoded, use_bytes=use_bytes
    )

    assert expected == response_output


@pytest.mark.parametrize(
    "decoded, use_bytes, expected",
    [
        (
            ["hello world"],
            True,
            ResponseOutput(
                name="foo", shape=[1, 1], datatype="BYTES", data=[b"hello world"]
            ),
        ),
        (
            ["hey", "whats"],
            True,
            ResponseOutput(
                name="foo", shape=[2, 1], datatype="BYTES", data=[b"hey", b"whats"]
            ),
        ),
        (
            ["hey", "whats"],
            False,
            ResponseOutput(
                name="foo", shape=[2, 1], datatype="BYTES", data=["hey", "whats"]
            ),
        ),
    ],
)
def test_encode_input(decoded, use_bytes, expected):
    response_output = StringCodec.encode_output(
        name="foo", payload=decoded, use_bytes=use_bytes
    )
    request_input = StringCodec.encode_input(
        name="foo", payload=decoded, use_bytes=use_bytes
    )

    assert request_input.data == response_output.data
    assert response_output.datatype == request_input.datatype
    assert request_input.parameters.content_type == StringCodec.ContentType
