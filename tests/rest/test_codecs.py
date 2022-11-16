import pytest
import numpy as np
import json

from typing import Any

from mlserver.types import Parameters
from mlserver.codecs import NumpyCodec, StringCodec, InputCodec, Base64Codec
from mlserver.rest.responses import Response


@pytest.mark.parametrize(
    "decoded, codec, expected",
    [
        (
            np.array([21.0]),
            NumpyCodec,
            {
                "name": "output-0",
                "datatype": "FP64",
                "shape": [1, 1],
                "data": [21.0],
            },
        ),
        (
            np.array([[b"\x01"], [b"\x02"]], dtype=bytes),
            NumpyCodec,
            {
                "name": "output-0",
                "datatype": "BYTES",
                "shape": [2, 1],
                "data": ["\x01\x02"],
            },
        ),
        (
            ["hey", "what's", "up"],
            StringCodec,
            {
                "name": "output-0",
                "datatype": "BYTES",
                "shape": [3, 1],
                "parameters": Parameters(content_type=StringCodec.ContentType),
                "data": ["hey", "what's", "up"],
            },
        ),
        (
            [b"Python is fun"],
            Base64Codec,
            {
                "name": "output-0",
                "datatype": "BYTES",
                "shape": [1, 1],
                "data": ["UHl0aG9uIGlzIGZ1bg=="],
            },
        ),
    ],
)
def test_encode_output_tensor(decoded: Any, codec: InputCodec, expected: dict):
    # Serialise response into final output bytes
    payload = codec.encode_output(name="output-0", payload=decoded)
    response = Response(content=None)
    rendered_as_bytes = response.render(payload.dict())

    # Decode response back into JSON and check if it matches the expected one
    rendered = rendered_as_bytes.decode("utf8")
    loaded_back = json.loads(rendered)
    assert loaded_back == expected
