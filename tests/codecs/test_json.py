import pytest

from typing import Any, Union

from mlserver.codecs.json import decode_from_bytelike_json_to_dict, encode_to_json_bytes


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
