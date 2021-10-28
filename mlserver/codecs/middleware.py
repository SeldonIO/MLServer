from typing import Dict

from .utils import decode_inference_request
from ..settings import ModelSettings
from ..types import InferenceRequest, MetadataTensor

DecodedParameterName = "_decoded_payload"


# TODO: Memoize to avoid computing the index every time
def _metadata_index(model_settings: ModelSettings) -> Dict[str, MetadataTensor]:
    index: Dict[str, MetadataTensor] = {}

    if not model_settings.inputs:
        return index

    for inp in model_settings.inputs:
        index[inp.name] = inp

    return index


def codec_middleware(
    request: InferenceRequest, model_settings: ModelSettings
) -> InferenceRequest:
    metadata_inputs = _metadata_index(model_settings)
    decode_inference_request(request, model_settings, metadata_inputs)

    return request
