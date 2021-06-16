import pytest
import numpy as np

from mlserver.codecs.numpy import _to_datatype

from mlserver_mlflow.encoding import (
    MLflowPayload,
    DefaultOutputName,
    to_outputs,
)


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
        assert output.data.__root__ == value.tolist()
        assert output.datatype == _to_datatype(value.dtype)
        assert output.shape == list(value.shape)
