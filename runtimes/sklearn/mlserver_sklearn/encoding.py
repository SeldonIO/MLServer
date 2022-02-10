from dataclasses import dataclass
from typing import List, Union

import numpy as np
import pandas as pd

from mlserver.codecs import NumpyCodec, PandasCodec
from mlserver.errors import InferenceError
from mlserver.types import RequestOutput, ResponseOutput

# TODO: more support!
SKLearnResponse = Union[np.ndarray, pd.DataFrame]


@dataclass
class SKLearnPayload:
    """Class for keeping track of requested outputs
    and corresponding model responses."""

    requested_output: RequestOutput
    model_output: SKLearnResponse


def to_outputs(sklearn_payloads: List[SKLearnPayload]) -> List[ResponseOutput]:
    """
    Encodes a list of SKLearn payloads into a list of proto-able ResponseOutputs.

    :param sklearn_payloads: List of requested outputs + the responses from the
        SKLearn model
    :return: response_outputs: List of encoded response outputs
    :raises: InferenceError if multiple columnar responses were returned by the model
    """
    response_outputs = []

    all_output_names = [p.requested_output.name for p in sklearn_payloads]

    for payload in sklearn_payloads:
        if _is_columnar_data(payload) and len(sklearn_payloads) > 1:
            raise InferenceError(
                f"{payload.requested_output.name} returned columnar data of type"
                f" {type(payload.model_output)} and {all_output_names} were"
                f" requested. Cannot encode multiple columnar data responses"
                f" one response."
            )

        if isinstance(payload.model_output, pd.DataFrame):
            # Immediately return the outputs of columnar data encoding,
            # don't try to jam more outputs together in one response.
            return PandasCodec.encode("some-model", payload.model_output).outputs

        response_output = NumpyCodec.encode(
            name=payload.requested_output.name, payload=payload.model_output
        )
        response_outputs.append(response_output)

    return response_outputs


def _is_columnar_data(payload: SKLearnPayload) -> bool:
    return isinstance(payload.model_output, pd.DataFrame)
