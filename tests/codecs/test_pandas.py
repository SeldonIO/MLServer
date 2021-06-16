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
                        name="b",
                        data=b"hello world",
                        datatype="BYTES",
                        shape=[1, 11],
                        parameters=Parameters(decoded_payload=["hello world"]),
                    ),
                ]
            ),
            pd.DataFrame({"a": [np.array([1, 2, 3])], "b": ["hello world"]}),
        ),
        (
            InferenceRequest(
                inputs=[
                    RequestInput(
                        name="a",
                        data=[1, 2, 3],
                        datatype="FP32",
                        shape=[3, 1],
                        parameters=Parameters(
                            decoded_payload=np.array([[1], [2], [3]])
                        ),
                    ),
                    RequestInput(
                        name="b",
                        data=b"ABC",
                        datatype="BYTES",
                        shape=[3, 1],
                    ),
                ]
            ),
            pd.DataFrame(
                {
                    "a": [np.array([1]), np.array([2]), np.array([3])],
                    "b": [a for a in b"ABC"],
                }
            ),
        ),
    ],
)
def test_decode(inference_request, expected):
    codec = PandasCodec()
    decoded = codec.decode(inference_request)

    pd.testing.assert_frame_equal(decoded, expected)
