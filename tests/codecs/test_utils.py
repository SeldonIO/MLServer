import pytest
import numpy as np

from mlserver.types import InferenceRequest, RequestInput, Parameters
from mlserver.codecs.base import CodecError
from mlserver.codecs.utils import (
    FirstInputRequestCodec,
    DecodedParameterName,
)
from mlserver.codecs.numpy import NumpyRequestCodec


@pytest.mark.parametrize(
    "inference_request, expected",
    [
        (
            InferenceRequest(
                inputs=[
                    RequestInput(
                        name="foo", shape=[2, 2], data=[1, 2, 3, 4], datatype="INT32"
                    )
                ]
            ),
            np.array([[1, 2], [3, 4]]),
        ),
        (
            InferenceRequest(
                inputs=[
                    RequestInput(
                        name="foo",
                        shape=[2, 2],
                        data=[1, 2, 3, 4],
                        datatype="INT32",
                        parameters=Parameters(**{DecodedParameterName: np.array([23])}),
                    )
                ]
            ),
            np.array([23]),
        ),
    ],
)
def test_first_input_decode(inference_request: InferenceRequest, expected: np.ndarray):
    inference_request.inputs = [inference_request.inputs[0]]
    first_input = NumpyRequestCodec.decode(inference_request)

    np.testing.assert_equal(first_input, expected)


def test_first_input_error(inference_request: InferenceRequest):
    with pytest.raises(CodecError):
        FirstInputRequestCodec.decode(inference_request)
