import numpy as np

from mlserver_mlflow.encoding import to_tensor_dict


def test_to_tensor_dict(inference_request):
    tensor_dict = to_tensor_dict(inference_request)

    expected_dict = {"input-0": np.array([1, 2, 3], dtype=np.int32)}

    assert tensor_dict.keys() == expected_dict.keys()
    for key, val in tensor_dict.items():
        expected_val = expected_dict[key]
        np.testing.assert_array_equal(val, expected_val)
