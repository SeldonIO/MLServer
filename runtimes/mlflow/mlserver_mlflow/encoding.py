import numpy as np

from typing import Dict, List, Union
from mlserver.codecs import NumpyCodec
from mlserver.types import RequestInput, ResponseOutput

DefaultOutputName = "predict"

TensorDict = Dict[str, np.ndarray]
MLflowPayload = Union[np.ndarray, TensorDict]


def to_tensor_dict(inputs: List[RequestInput]) -> TensorDict:
    tensor_dict = {}
    codec = NumpyCodec()

    for model_input in inputs:
        tensor_dict[model_input.name] = codec.decode(model_input)

    return tensor_dict


def to_outputs(mlflow_payload: MLflowPayload) -> List[ResponseOutput]:
    codec = NumpyCodec()

    if type(mlflow_payload) is np.ndarray:
        # Cast to dict of tensors
        mlflow_payload = {DefaultOutputName: mlflow_payload}  # type: ignore

    return [
        codec.encode(key, value)
        for key, value in mlflow_payload.items()  # type: ignore
    ]
