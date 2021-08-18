import numpy as np

from typing import Dict, List, Union

import pandas as pd

from mlserver.codecs import NumpyCodec, PandasCodec
from mlserver.types import ResponseOutput

DefaultOutputName = "predict"

TensorDict = Dict[str, np.ndarray]
MLflowPayload = Union[np.ndarray, pd.DataFrame, pd.Series, TensorDict]


def to_outputs(mlflow_payload: MLflowPayload) -> List[ResponseOutput]:
    codec = NumpyCodec()

    if isinstance(mlflow_payload, np.ndarray) \
            or isinstance(mlflow_payload, pd.DataFrame) \
            or isinstance(mlflow_payload, pd.Series):

        # convert pandas Series or DataFrame to numpy ndarray
        if isinstance(mlflow_payload, pd.DataFrame):
            assert isinstance(mlflow_payload, pd.DataFrame)
            mlflow_payload = mlflow_payload.to_numpy()
        elif isinstance(mlflow_payload, pd.Series):
            assert isinstance(mlflow_payload, pd.Series)
            mlflow_payload = mlflow_payload.to_numpy()

        # Cast to dict of tensor
        mlflow_payload = {DefaultOutputName: mlflow_payload}  # type: ignore

    return [
        codec.encode(key, value)
        for key, value in mlflow_payload.items()  # type: ignore
    ]
