import numpy as np

from typing import Dict, List, Union
from mlserver.utils import to_ndarray, to_datatype
from mlserver.types import RequestInput, ResponseOutput

DefaultOutputName = "predict"

TensorDict = Dict[str, np.ndarray]
MLflowPayload = Union[np.ndarray, TensorDict]


def to_tensor_dict(inputs: List[RequestInput]) -> TensorDict:
    tensor_dict = {}

    for model_input in inputs:
        tensor_dict[model_input.name] = to_ndarray(model_input)

    return tensor_dict


def to_outputs(mlflow_payload: MLflowPayload) -> List[ResponseOutput]:
    if type(mlflow_payload) is np.ndarray:
        # Cast to dict of tensors
        mlflow_payload = {DefaultOutputName: mlflow_payload}  # type: ignore

    return [
        ResponseOutput(
            name=key,
            shape=value.shape,
            datatype=to_datatype(value.dtype),
            data=value.tolist(),
        )
        for key, value in mlflow_payload.items()  # type: ignore
    ]
