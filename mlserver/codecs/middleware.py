from typing import Any, Optional, Dict

from .base import find_input_codec, find_request_codec
from ..settings import ModelSettings
from ..types import InferenceRequest, RequestInput, MetadataTensor, Parameters

DecodedParameterName = "_decoded_payload"


def _get_content_type(parametrised_obj, tagged_obj=None) -> Optional[str]:
    if parametrised_obj.parameters and parametrised_obj.parameters.content_type:
        return parametrised_obj.parameters.content_type

    if tagged_obj and tagged_obj.tags and tagged_obj.tags.content_type:
        return tagged_obj.tags.content_type

    return None


def _save_decoded(parametrised_obj, decoded_payload: Any):
    if not parametrised_obj.parameters:
        parametrised_obj.parameters = Parameters()

    setattr(parametrised_obj.parameters, DecodedParameterName, decoded_payload)


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


def codec_middleware(
    request: InferenceRequest, model_settings: ModelSettings
) -> InferenceRequest:
    metadata_inputs = _metadata_index(model_settings)
    for request_input in request.inputs:
        decoded_payload = _decode_request_input(request_input, metadata_inputs)
        _save_decoded(request_input, decoded_payload)

    # TODO: Pass metadata once it contains tags
    request_content_type = _get_content_type(request)
    if request_content_type is not None:
        codec = find_request_codec(request_content_type)
        if codec is not None:
            decoded_payload = codec.decode(request)
            _save_decoded(request, decoded_payload)

    return request
