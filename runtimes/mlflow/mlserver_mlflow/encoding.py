import numpy as np

from typing import Dict
from mlserver.utils import to_ndarray
from mlserver.types import InferenceRequest

TensorDict = Dict[str, np.ndarray]


def to_tensor_dict(payload: InferenceRequest) -> TensorDict:
    tensor_dict = {}

    for model_input in payload.inputs:
        tensor_dict[model_input.name] = to_ndarray(model_input)

    return tensor_dict
