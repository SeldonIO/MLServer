import pytest

from mlserver.codecs import StringCodec
from mlserver.types import RequestInput


@pytest.mark.parametrize(
    "encoded, payload",
    [
        (b"hello world", "hello world"),
    ],
)
def test_string_codec(encoded, payload):
    request_input = RequestInput(name="foo", shape=[], datatype="BYTES", data=encoded)
    codec = StringCodec()
    decoded = codec.decode(request_input)

    assert decoded == payload

    response_output = codec.encode(name="foo", payload=decoded)

    assert response_output.datatype == "BYTES"
    assert response_output.shape == [len(encoded)]
    assert response_output.data.__root__ == encoded
