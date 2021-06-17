import numpy as np

from mlserver.types import InferenceRequest
from mlserver_mlflow.codecs import TensorDictCodec


def test_decode(inference_request: InferenceRequest):
    codec = TensorDictCodec()
    tensor_dict = codec.decode(inference_request)

    expected_dict = {"input-0": np.array([1, 2, 3], dtype=np.int32)}

    assert tensor_dict.keys() == expected_dict.keys()
    for key, val in tensor_dict.items():
        expected_val = expected_dict[key]
        np.testing.assert_array_equal(val, expected_val)
