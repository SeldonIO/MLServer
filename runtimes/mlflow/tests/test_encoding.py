import numpy as np
import pandas as pd
import pytest
from mlserver_mlflow.encoding import (
    MLflowPayload,
    to_outputs,
    _convert_to_tensor_data_if_raw,
)

from mlserver.codecs.numpy import _to_datatype


@pytest.mark.parametrize(
    "mlflow_payload",
    [
        np.array([1, 2, 3]),
        {"foo": np.array([1, 2, 3])},
        {"foo": np.array([1, 2, 3]), "bar": np.array([4, 5, 6], dtype=np.float32)},
        pd.DataFrame([[1, 2, 3]]),
        pd.DataFrame([[1, 2, 3], [4, 5, 6]]),
        pd.Series([1, 2, 3]),
    ],
)
def test_to_outputs(mlflow_payload: MLflowPayload):
    initial_payload = mlflow_payload
    outputs = to_outputs(mlflow_payload)

    mlflow_payload = _convert_to_tensor_data_if_raw(mlflow_payload)

    assert len(outputs) == len(mlflow_payload)
    for output in outputs:
        value = mlflow_payload[output.name]
        if isinstance(initial_payload, pd.DataFrame):
            # the response data is flatten
            assert output.data.__root__ == value.flatten().tolist()
        else:
            assert output.data.__root__ == value.tolist()
        assert output.datatype == _to_datatype(value.dtype)
        assert output.shape == list(value.shape)
