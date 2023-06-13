import numpy as np

from typing import Optional, Dict

from mlserver.types import InferenceRequest, InferenceResponse, Parameters
from mlserver.codecs import (
    NumpyCodec,
    RequestCodec,
    register_request_codec,
    get_decoded_or_raw,
)
from mlserver.codecs.lists import is_list_of

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
    def encode_response(
        cls,
        model_name: str,
        payload: TensorDict,
        model_version: Optional[str] = None,
        **kwargs
    ) -> InferenceResponse:
        outputs = [
            NumpyCodec.encode_output(name, value, **kwargs)
            for name, value in payload.items()
        ]

        return InferenceResponse(
            model_name=model_name,
            model_version=model_version,
            outputs=outputs,
            parameters=Parameters(content_type=cls.ContentType),
        )

    @classmethod
    def decode_response(cls, response: InferenceResponse) -> TensorDict:
        return {
            response_output.name: NumpyCodec.decode_output(response_output)
            for response_output in response.outputs
        }

    @classmethod
    def encode_request(cls, payload: TensorDict, **kwargs) -> InferenceRequest:
        inputs = [
            NumpyCodec.encode_input(name, value, **kwargs)
            for name, value in payload.items()
        ]

        return InferenceRequest(
            inputs=inputs, parameters=Parameters(content_type=cls.ContentType)
        )

    @classmethod
    def decode_request(cls, request: InferenceRequest) -> TensorDict:
        return {
            request_input.name: get_decoded_or_raw(request_input)
            for request_input in request.inputs
        }
