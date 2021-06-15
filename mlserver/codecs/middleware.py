from typing import Any, Optional, Dict

from .base import find_input_codec
from ..settings import ModelSettings
from ..types import InferenceRequest, RequestInput, MetadataTensor, Parameters

DecodedParameterName = "decoded_payload"


def _get_content_type(
    request_input: RequestInput, input_metadata: Optional[MetadataTensor]
) -> Optional[str]:
    if request_input.parameters and request_input.parameters.content_type:
        return request_input.parameters.content_type

    if input_metadata and input_metadata.tags and input_metadata.tags.content_type:
        return input_metadata.tags.content_type

    return None


# TODO: Memoize to avoid computing the index every time
def _metadata_index(model_settings: ModelSettings) -> Dict[str, MetadataTensor]:
    index: Dict[str, MetadataTensor] = {}

    if not model_settings.inputs:
        return index

    for inp in model_settings.inputs:
        index[inp.name] = inp

    return index


def _decode_request_input(
    request_input: RequestInput, metadata_inputs: Dict[str, MetadataTensor]
) -> Optional[Any]:
    input_metadata = metadata_inputs.get(request_input.name)
    content_type = _get_content_type(request_input, input_metadata)
    if content_type is None:
        return None

    codec = find_input_codec(content_type)
    if codec is None:
        return None

    return codec.decode(request_input)


def decode_request_inputs(
    request: InferenceRequest, model_settings: ModelSettings
) -> InferenceRequest:
    metadata_inputs = _metadata_index(model_settings)
    for request_input in request.inputs:
        decoded_payload = _decode_request_input(request_input, metadata_inputs)
        if not request_input.parameters:
            request_input.parameters = Parameters()

        setattr(request_input.parameters, DecodedParameterName, decoded_payload)

    return request
