import pytest
import pandas as pd
import numpy as np

from mlserver.codecs.pandas import PandasCodec
from mlserver.types import InferenceRequest, RequestInput, Parameters


@pytest.mark.parametrize(
    "inference_request, expected",
    [
        (
            InferenceRequest(
                inputs=[
                    RequestInput(
                        name="a",
                        data=[1, 2, 3],
                        datatype="FP32",
                        shape=[1, 3],
                        parameters=Parameters(decoded_payload=np.array([[1, 2, 3]])),
                    ),
                    RequestInput(
                        name="b", data=b"hello world", datatype="BYTES", shape=[11]
                    ),
                ]
            ),
            pd.DataFrame({"a": [np.array([1, 2, 3])], "b": ["hello world"]}),
        ),
    ],
)
def test_decode(inference_request, expected):
    codec = PandasCodec()
    decoded = codec.decode(inference_request)

    assert decoded == expected
