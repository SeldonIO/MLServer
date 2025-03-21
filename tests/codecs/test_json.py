import pytest
import numpy as np

from typing import Any, List, Union

from mlserver.types import RequestInput, ResponseOutput
from mlserver.codecs.json import (
    decode_from_bytelike_json_to_dict,
    encode_to_json_bytes,
    encode_to_json,
    decode_json_input_or_output,
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
        (
            [[1, 2, 3]],
            [b"[1,2,3]"],
        ),
        (
            [[1], [2, 3], [4, 5, 6]],
            [b"[1]", b"[2,3]", b"[4,5,6]"],
        ),
        (
            [{"a": 1, "b": 2}],
            [b'{"a":1,"b":2}'],
        ),
        (
            [{"a": 1}, {"b": 2, "c": 3}],
            [b'{"a":1}', b'{"b":2,"c":3}'],
        ),
        (
            [np.array([1, 2, 3])],
            [b"[1,2,3]"],
        ),
    ],
)
def test_encode_to_json(payload: List[Any], expected: ResponseOutput):
    response_output = [encode_to_json(elem) for elem in payload]
    assert response_output == expected


@pytest.mark.parametrize(
    "input_or_output, expected",
    [
        (
            RequestInput(
                name="foo",
                shape=[1, 1],
                data=[b"[1,2,3]"],
                datatype="BYTES",
            ),
            [[1, 2, 3]],
        ),
        (
            RequestInput(
                name="foo",
                shape=[3, 1],
                data=[b"[1]", b"[2,3]", b"[4,5,6]"],
                datatype="BYTES",
            ),
            [[1], [2, 3], [4, 5, 6]],
        ),
        (
            RequestInput(
                name="foo",
                shape=[1, 1],
                data=[b'{"a":1,"b":2}'],
                datatype="BYTES",
            ),
            [{"a": 1, "b": 2}],
        ),
        (
            RequestInput(
                name="foo",
                shape=[2, 1],
                data=[b'{"a":1}', b'{"b":2,"c":3}'],
                datatype="BYTES",
            ),
            [{"a": 1}, {"b": 2, "c": 3}],
        ),
        (
            ResponseOutput(
                name="foo",
                shape=[1, 1],
                data=[b"[1,2,3]"],
                datatype="BYTES",
            ),
            [[1, 2, 3]],
        ),
        (
            ResponseOutput(
                name="foo",
                shape=[3, 1],
                data=[b"[1]", b"[2,3]", b"[4,5,6]"],
                datatype="BYTES",
            ),
            [[1], [2, 3], [4, 5, 6]],
        ),
        (
            ResponseOutput(
                name="foo",
                shape=[1, 1],
                data=[b'{"a":1,"b":2}'],
                datatype="BYTES",
            ),
            [{"a": 1, "b": 2}],
        ),
        (
            ResponseOutput(
                name="foo",
                shape=[2, 1],
                data=[b'{"a":1}', b'{"b":2,"c":3}'],
                datatype="BYTES",
            ),
            [{"a": 1}, {"b": 2, "c": 3}],
        ),
    ],
)
def test_decode_json_input_or_output(
    input_or_output: Union[RequestInput, ResponseOutput], expected: Any
):
    assert expected == decode_json_input_or_output(input_or_output)
