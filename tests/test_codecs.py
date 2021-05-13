import pytest

from mlserver.codecs import StringCodec
from mlserver.types import RequestInput, ResponseOutput


@pytest.mark.parametrize(
    "encoded,payload",
    [
        (b"hello world", "hello world"),
    ],
)
def test_string_codec_encode(payload, encoded):
    codec = StringCodec()

    request_input = RequestInput(name="foo", shape=[], datatype="BYTES", data=encoded)
    decoded = codec.decode(request_input)

    assert decoded == payload

    response_output = ResponseOutput(name="foo", shape=[], datatype="INT32", data=[])
    response_output = codec.encode(decoded, response_output)

    assert response_output.datatype == "BYTES"
    assert response_output.shape == [len(encoded)]
    assert response_output.data.__root__ == encoded
