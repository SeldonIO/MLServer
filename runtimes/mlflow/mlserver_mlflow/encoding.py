from typing import Dict, List, Union

import numpy as np
import pandas as pd

from mlserver.codecs import NumpyCodec
from mlserver.types import ResponseOutput

DefaultOutputName = "predict"

TensorDict = Dict[str, np.ndarray]
MLflowPayload = Union[np.ndarray, pd.DataFrame, pd.Series, TensorDict]


def to_outputs(mlflow_payload: MLflowPayload) -> List[ResponseOutput]:
    codec = NumpyCodec()

    mlflow_payload = _convert_to_tensor_data_if_raw(mlflow_payload)

    return [
        codec.encode(key, value)
        for key, value in mlflow_payload.items()  # type: ignore
    ]


def _convert_to_tensor_data_if_raw(mlflow_payload: MLflowPayload) -> MLflowPayload:
    # if the payload is ndarray, dataframe or series, convert it to `TensorDict`
    # we also convert `pd.DataFrame` and `pd.Series` to `np.ndarray`
    if (
        isinstance(mlflow_payload, np.ndarray)
        or isinstance(mlflow_payload, pd.DataFrame)
        or isinstance(mlflow_payload, pd.Series)
    ):

        # convert pandas Series or DataFrame to numpy ndarray
        if isinstance(mlflow_payload, pd.DataFrame):
            mlflow_payload_array = mlflow_payload.to_numpy()
        elif isinstance(mlflow_payload, pd.Series):
            mlflow_payload_array = mlflow_payload.to_numpy()
        else:
            mlflow_payload_array = mlflow_payload

        # Cast to dict of tensor
        return {DefaultOutputName: mlflow_payload_array}

    return mlflow_payload
