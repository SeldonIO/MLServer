import pytest
import numpy as np

from typing import Any

from mlserver.types import InferenceRequest, ResponseOutput
from mlserver_mlflow.codecs import TensorDictCodec


@pytest.mark.parametrize(
    "payload, expected",
    [
        ({"foo": np.array([1, 2, 3])}, True),
        ({"foo": np.array([1, 2, 3]), "bar": np.array([3.4])}, True),
        ({"foo": np.array([1, 2, 3]), "bar": [3.4]}, False),
        ({"foo": [3.4]}, False),
        ({"a": 0}, False),
        ([3, 4], False),
        (np.array([3, 4]), False),
    ],
)
def test_can_encode(payload: Any, expected: bool):
    assert TensorDictCodec.can_encode(payload) == expected


def test_encode():
    model_name = "dummy-model"
    payload = {"foo": np.array([1, 2, 3]), "bar": np.array([[2.3], [4.5]])}
    inference_response = TensorDictCodec.encode(model_name, payload)

    assert inference_response.model_name == model_name
    assert len(inference_response.outputs) == 2
    assert inference_response.outputs[0] == ResponseOutput(
        name="foo", datatype="INT64", shape=[3], data=[1, 2, 3]
    )
    assert inference_response.outputs[1] == ResponseOutput(
        name="bar", datatype="FP64", shape=[2, 1], data=[2.3, 4.5]
    )


def test_decode(inference_request: InferenceRequest):
    tensor_dict = TensorDictCodec.decode(inference_request)

    expected_dict = {"foo": np.array([1, 2, 3], dtype=np.int32)}

    assert tensor_dict.keys() == expected_dict.keys()
    for key, val in tensor_dict.items():
        expected_val = expected_dict[key]
        np.testing.assert_array_equal(val, expected_val)
