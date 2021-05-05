import pytest
import numpy as np

from mlserver.utils import to_datatype

from mlserver_mlflow.encoding import (
    MLflowPayload,
    DefaultOutputName,
    to_tensor_dict,
    to_outputs,
)


def test_to_tensor_dict(inference_request):
    tensor_dict = to_tensor_dict(inference_request.inputs)

    expected_dict = {"input-0": np.array([1, 2, 3], dtype=np.int32)}

    assert tensor_dict.keys() == expected_dict.keys()
    for key, val in tensor_dict.items():
        expected_val = expected_dict[key]
        np.testing.assert_array_equal(val, expected_val)


@pytest.mark.parametrize(
    "mlflow_payload",
    [
        np.array([1, 2, 3]),
        {"foo": np.array([1, 2, 3])},
        {"foo": np.array([1, 2, 3]), "bar": np.array([4, 5, 6], dtype=np.float32)},
    ],
)
def test_to_outputs(mlflow_payload: MLflowPayload):
    outputs = to_outputs(mlflow_payload)

    if type(mlflow_payload) == np.ndarray:
        mlflow_payload = {DefaultOutputName: mlflow_payload}  # type: ignore

    assert len(outputs) == len(mlflow_payload)
    for output in outputs:
        value = mlflow_payload[output.name]
        assert output.data == value.tolist()
        assert output.datatype == to_datatype(value.dtype)
        assert output.shape == list(value.shape)
