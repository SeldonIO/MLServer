import numpy as np

from typing import Dict

from mlserver.types import InferenceRequest, InferenceResponse
from mlserver.codecs import (
    NumpyCodec,
    RequestCodec,
    register_request_codec,
    get_decoded_or_raw,
)
from mlserver.codecs.utils import is_list_of

from typing import Any


TensorDict = Dict[str, np.ndarray]


@register_request_codec
class TensorDictCodec(RequestCodec):
    """
    The TensorDictCodec knows how to encode / decode a dictionary of tensors.
    """

    ContentType = "dict"

    @classmethod
    def can_encode(cls, payload: Any) -> bool:
        if not isinstance(payload, dict):
            return False

        return is_list_of(list(payload.values()), np.ndarray)

    @classmethod
    def encode(
        cls, model_name: str, payload: TensorDict, model_version: str = None
    ) -> InferenceResponse:
        outputs = [NumpyCodec.encode(name, value) for name, value in payload.items()]

        return InferenceResponse(
            model_name=model_name, model_version=model_version, outputs=outputs
        )

    @classmethod
    def decode(cls, request: InferenceRequest) -> TensorDict:
        return {
            request_input.name: get_decoded_or_raw(request_input)
            for request_input in request.inputs
        }
