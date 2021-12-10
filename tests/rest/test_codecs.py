import pytest
import numpy as np
import json

from typing import Any

from mlserver.codecs import NumpyCodec, StringCodec, InputCodec
from mlserver.types import RequestInput
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
                "shape": [1],
                "parameters": None,
                "data": [21.0],
            },
        ),
        (
            ["hey", "what's", "up"],
            StringCodec,
            {
                "name": "output-0",
                "datatype": "BYTES",
                "shape": [3],
                "parameters": None,
                "data": ["hey", "what's", "up"],
            },
        ),
    ],
)
def test_encode_output_tensor(decoded: Any, codec: InputCodec, expected: dict):
    # Serialise response into final output bytes
    payload = codec.encode(name="output-0", payload=decoded)
    response = Response()
    rendered_as_bytes = response.render(payload.dict())

    # Decode response back into JSON and check if it matches the expected one
    rendered = rendered_as_bytes.decode("utf8")
    loaded_back = json.loads(rendered)
    assert loaded_back == expected
