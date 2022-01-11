from dataclasses import dataclass
from typing import Dict, List, Union

import numpy as np
import pandas as pd

from mlserver import types
from mlserver.codecs import NumpyCodec, PandasCodec
from mlserver.errors import InferenceError
from mlserver.types import ResponseOutput, InferenceResponse

SKLearnResponse = Union[np.ndarray, pd.DataFrame, pd.Series]

@dataclass
class SKLearnPayload():
    """Class for keeping track of requested outputs and corresponding model responses."""
    requested_output: ResponseOutput
    model_output: SKLearnResponse


def to_response(model_name: str,
                model_version: str,
                sklearn_payloads: List[SKLearnPayload]) -> InferenceResponse:
    """
    Encodes a list of SKLearn payloads into a single InferenceResponse for the wire.

    :param model_name: Name of the model for the InferenceResponse
    :param model_version: Version of hte model for the InferenceResponse
    :param sklearn_payloads: List of requested outputs + the responses from the SKLearn model
    :return:
    """
    if len(sklearn_payloads) == 1 and isinstance(sklearn_payloads[0].model_output, pd.DataFrame):
        return PandasCodec.encode(model_name=model_name,
                                  model_version=model_version,
                                  payload=sklearn_payloads[0].model_output)

    return types.InferenceResponse(
        model_name=model_name,
        model_version=model_version,
        outputs=to_outputs(sklearn_payloads)
    )


def to_outputs(sklearn_payloads: List[SKLearnPayload]) -> List[ResponseOutput]:
    """
    Encodes a list of SKLearn payloads into a list of proto-able ResponseOutputs.
    Assumes every model payload can be encoded into a single ResponseOutput,
    no columnar data like DataFrames are allowed.

    :param sklearn_payloads: List of requested outputs + the responses from the SKLearn model
    :return: response_outputs: List of encoded response outputs
    """
    response_outputs = []

    all_output_names = [p.requested_output.name for p in sklearn_payloads]

    for payload in sklearn_payloads:
        if isinstance(payload.model_output, pd.DataFrame):
            raise InferenceError(f"{payload.requested_output.name} is of type DataFrame and "
                                 f"{all_output_names} were requested. Cannot encode multiple "
                                 f"DataFrames in one response. "
                                 f"Please request only a single DataFrame output.")

        # TODO: accommodate more things like Strings
        response_output = NumpyCodec.encode(name=payload.requested_output.name,
                                            payload=payload.model_output)
        response_outputs.append(response_output)

    return response_outputs

