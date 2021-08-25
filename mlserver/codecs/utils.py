from typing import Any, Union, Dict, Optional, Type

from ..types import (
    InferenceRequest,
    InferenceResponse,
    RequestInput,
    MetadataTensor,
    Parameters,
)
from .base import (
    find_input_codec,
    find_request_codec,
    InputCodec,
    RequestCodec,
    CodecError,
)

Parametrised = Union[InferenceRequest, RequestInput]
Tagged = Union[MetadataTensor]
DecodedParameterName = "_decoded_payload"


def _get_content_type(
    parametrised_obj: Parametrised, tagged_obj: Optional[Tagged] = None
) -> Optional[str]:
    if parametrised_obj.parameters and parametrised_obj.parameters.content_type:
        return parametrised_obj.parameters.content_type

    if tagged_obj is not None:
        if tagged_obj.tags and tagged_obj.tags.content_type:
            return tagged_obj.tags.content_type

    return None


def _save_decoded(parametrised_obj: Parametrised, decoded_payload: Any):
    if not parametrised_obj.parameters:
        parametrised_obj.parameters = Parameters()

    setattr(parametrised_obj.parameters, DecodedParameterName, decoded_payload)


def decode_request_input(
    request_input: RequestInput,
    metadata_inputs: Dict[str, MetadataTensor],
) -> Optional[Any]:
    input_metadata = metadata_inputs.get(request_input.name)
    content_type = _get_content_type(request_input, input_metadata)
    if content_type is None:
        return None

    codec = find_input_codec(content_type)
    if codec is None:
        return None

    decoded_payload = codec.decode(request_input)
    _save_decoded(request_input, decoded_payload)
    return decoded_payload


def decode_inference_request(
    inference_request: InferenceRequest, metadata_inputs: Dict[str, MetadataTensor]
) -> Optional[Any]:
    for request_input in inference_request.inputs:
        decode_request_input(request_input, metadata_inputs)

    request_content_type = _get_content_type(inference_request)
    if request_content_type is not None:
        codec = find_request_codec(request_content_type)
        if codec is not None:
            decoded_payload = codec.decode(inference_request)
            _save_decoded(inference_request, decoded_payload)
            return decoded_payload

    return inference_request


def has_decoded(parametrised_obj: Parametrised) -> bool:
    if parametrised_obj.parameters:
        return hasattr(parametrised_obj.parameters, DecodedParameterName)

    return False


def get_decoded(parametrised_obj: Parametrised) -> Any:
    if has_decoded(parametrised_obj):
        return getattr(parametrised_obj.parameters, DecodedParameterName)


def get_decoded_or_raw(parametrised_obj: Parametrised) -> Any:
    if not has_decoded(parametrised_obj):
        if isinstance(parametrised_obj, RequestInput):
            # If this is a RequestInput, return its data
            return parametrised_obj.data

        # Otherwise, return full object
        return parametrised_obj

    return get_decoded(parametrised_obj)


class FirstInputRequestCodec(RequestCodec):
    """
    The FirstInputRequestCodec can be used as a "meta-implementation" for other
    codecs. Its goal to decode the whole request simply as the first decoded
    element.
    """

    InputCodec: Optional[Type[InputCodec]] = None

    @classmethod
    def encode(
        cls, model_name: str, payload: Any, model_version: str = None
    ) -> InferenceResponse:
        output = InputCodec.encode("output-1", payload)
        return InferenceResponse(
            model_name=model_name, model_version=model_version, outputs=[output]
        )

    @classmethod
    def decode(cls, request: InferenceRequest) -> Any:
        if len(request.inputs) != 1:
            raise CodecError(
                f"The '{cls.ContentType}' codec only supports a single input tensor "
                f"({len(request.inputs)} were received)"
            )

        first_input = request.inputs[0]
        if not has_decoded(first_input):
            decoded_payload = cls.InputCodec.decode(first_input)  # type: ignore
            _save_decoded(first_input, decoded_payload)

        return get_decoded_or_raw(first_input)
