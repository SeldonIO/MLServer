import pytest
import numpy as np

from typing import Any, Union

from mlserver.types import RequestInput, ResponseOutput, Parameters
from mlserver.codecs.json import (
    decode_from_bytelike_json_to_dict,
    encode_to_json_bytes,
    JSONCodec,
)


@pytest.mark.parametrize(
    "input, expected",
    [
        (b"{}", dict()),
        ("{}", dict()),
        ('{"hello":"world"}', {"hello": "world"}),
        (b'{"hello":"world"}', {"hello": "world"}),
        (b'{"hello":"' + "world".encode("utf-8") + b'"}', {"hello": "world"}),
        (
            b'{"hello":"' + "world".encode("utf-8") + b'", "foo": { "bar": "baz" } }',
            {"hello": "world", "foo": {"bar": "baz"}},
        ),
    ],
)
def test_decode_input(input: Union[str, bytes], expected: dict):
    assert expected == decode_from_bytelike_json_to_dict(input)


@pytest.mark.parametrize(
    # input and expected are flipped here for easier CTRL+C / V
    "expected, input",
    [
        (b"{}", dict()),
        (b'{"hello":"world"}', {"hello": "world"}),
        (b'{"hello":"' + "world".encode("utf-8") + b'"}', {"hello": "world"}),
        (
            b'{"hello":"' + "world".encode("utf-8") + b'","foo":{"bar":"baz"}}',
            {"hello": b"world", "foo": {"bar": "baz"}},
        ),
    ],
)
def test_encode_input(input: Any, expected: bytes):
    assert expected == encode_to_json_bytes(input)


@pytest.mark.parametrize(
    "payload, expected",
    [
        ([[1, 2, 3]], True),
        ([{"dummy_1": 1, "dummy_2": 2}], True),
        (
            [
                {"dummy_1": 1},
                {"dummy_2": [{"dummy_3": 3, "dummy_4": 4}, {"dummy_5": 5}]},
            ],
            True,
        ),
        ([np.array([1, 2, 3])], True),
        ([{1, 2, 3}], False),
    ],
)
def test_json_codec_can_encode(payload: Any, expected: bool):
    assert JSONCodec.can_encode(payload) == expected


@pytest.mark.parametrize(
    "payload, expected",
    [
        (
            [[1, 2, 3]],
            ResponseOutput(
                name="foo",
                shape=[1, 1],
                data=[b"[1,2,3]"],
                datatype="BYTES",
                parameters=Parameters(content_type=JSONCodec.ContentType),
            ),
        ),
        (
            [[1], [2, 3], [4, 5, 6]],
            ResponseOutput(
                name="foo",
                shape=[3, 1],
                data=[b"[1]", b"[2,3]", b"[4,5,6]"],
                datatype="BYTES",
                parameters=Parameters(content_type=JSONCodec.ContentType),
            ),
        ),
        (
            [{"a": 1, "b": 2}],
            ResponseOutput(
                name="foo",
                shape=[1, 1],
                data=[b'{"a":1,"b":2}'],
                datatype="BYTES",
                parameters=Parameters(content_type=JSONCodec.ContentType),
            ),
        ),
        (
            [{"a": 1}, {"b": 2, "c": 3}],
            ResponseOutput(
                name="foo",
                shape=[2, 1],
                data=[b'{"a":1}', b'{"b":2,"c":3}'],
                datatype="BYTES",
                parameters=Parameters(content_type=JSONCodec.ContentType),
            ),
        ),
    ],
)
def test_json_codec_encode_output(payload: Any, expected: ResponseOutput):
    response_output = JSONCodec.encode_output("foo", payload)
    assert response_output == expected


@pytest.mark.parametrize(
    "request_input, expected",
    [
        (
            ResponseOutput(
                name="foo",
                shape=[1, 1],
                data=[b"[1,2,3]"],
                datatype="BYTES",
                parameters=Parameters(content_type=JSONCodec.ContentType),
            ),
            [[1, 2, 3]],
        ),
        (
            ResponseOutput(
                name="foo",
                shape=[3, 1],
                data=[b"[1]", b"[2,3]", b"[4,5,6]"],
                datatype="BYTES",
                parameters=Parameters(content_type=JSONCodec.ContentType),
            ),
            [[1], [2, 3], [4, 5, 6]],
        ),
        (
            ResponseOutput(
                name="foo",
                shape=[1, 1],
                data=[b'{"a":1,"b":2}'],
                datatype="BYTES",
                parameters=Parameters(content_type=JSONCodec.ContentType),
            ),
            [{"a": 1, "b": 2}],
        ),
        (
            ResponseOutput(
                name="foo",
                shape=[2, 1],
                data=[b'{"a":1}', b'{"b":2,"c":3}'],
                datatype="BYTES",
                parameters=Parameters(content_type=JSONCodec.ContentType),
            ),
            [{"a": 1}, {"b": 2, "c": 3}],
        ),
    ],
)
def test_json_codec_decode_output(request_input: ResponseOutput, expected: Any):
    assert expected == JSONCodec.decode_output(request_input)


@pytest.mark.parametrize(
    "payload, expected",
    [
        (
            [[1, 2, 3]],
            RequestInput(
                name="foo",
                shape=[1, 1],
                data=[b"[1,2,3]"],
                datatype="BYTES",
                parameters=Parameters(content_type=JSONCodec.ContentType),
            ),
        ),
        (
            [[1], [2, 3], [4, 5, 6]],
            RequestInput(
                name="foo",
                shape=[3, 1],
                data=[b"[1]", b"[2,3]", b"[4,5,6]"],
                datatype="BYTES",
                parameters=Parameters(content_type=JSONCodec.ContentType),
            ),
        ),
        (
            [{"a": 1, "b": 2}],
            RequestInput(
                name="foo",
                shape=[1, 1],
                data=[b'{"a":1,"b":2}'],
                datatype="BYTES",
                parameters=Parameters(content_type=JSONCodec.ContentType),
            ),
        ),
        (
            [{"a": 1}, {"b": 2, "c": 3}],
            RequestInput(
                name="foo",
                shape=[2, 1],
                data=[b'{"a":1}', b'{"b":2,"c":3}'],
                datatype="BYTES",
                parameters=Parameters(content_type=JSONCodec.ContentType),
            ),
        ),
    ],
)
def test_json_codec_encode_input(payload: Any, expected: RequestInput):
    request_input = JSONCodec.encode_input("foo", payload)
    assert request_input == expected


@pytest.mark.parametrize(
    "request_input, expected",
    [
        (
            RequestInput(
                name="foo",
                shape=[1, 1],
                data=[b"[1,2,3]"],
                datatype="BYTES",
                parameters=Parameters(content_type=JSONCodec.ContentType),
            ),
            [[1, 2, 3]],
        ),
        (
            RequestInput(
                name="foo",
                shape=[3, 1],
                data=[b"[1]", b"[2,3]", b"[4,5,6]"],
                datatype="BYTES",
                parameters=Parameters(content_type=JSONCodec.ContentType),
            ),
            [[1], [2, 3], [4, 5, 6]],
        ),
        (
            RequestInput(
                name="foo",
                shape=[1, 1],
                data=[b'{"a":1,"b":2}'],
                datatype="BYTES",
                parameters=Parameters(content_type=JSONCodec.ContentType),
            ),
            [{"a": 1, "b": 2}],
        ),
        (
            RequestInput(
                name="foo",
                shape=[2, 1],
                data=[b'{"a":1}', b'{"b":2,"c":3}'],
                datatype="BYTES",
                parameters=Parameters(content_type=JSONCodec.ContentType),
            ),
            [{"a": 1}, {"b": 2, "c": 3}],
        ),
    ],
)
def test_json_codec_decode_input(request_input: RequestInput, expected: Any):
    assert expected == JSONCodec.decode_input(request_input)


@pytest.mark.parametrize(
    "request_input",
    [
        RequestInput(
            name="foo",
            shape=[1, 1],
            data=[b"[1,2,3]"],
            datatype="BYTES",
            parameters=Parameters(content_type=JSONCodec.ContentType),
        ),
    ],
)
def test_json_codec_idempotent(request_input: RequestInput):
    decoded = JSONCodec.decode_input(request_input)
    response_output = JSONCodec.encode_output(name="foo", payload=decoded)

    request_input_result = JSONCodec.encode_input(name="foo", payload=decoded)
    assert response_output.datatype == request_input_result.datatype
    assert response_output.shape == request_input_result.shape
    assert response_output.data == request_input_result.data

    if request_input_result.parameters is not None:
        assert request_input_result.parameters.content_type == JSONCodec.ContentType
