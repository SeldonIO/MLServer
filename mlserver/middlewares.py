from typing import Dict, Optional

from .types import Parameters, InferenceRequest, RequestInput, MetadataTensor
from .codecs import _codec_registry as codecs
from .model import MLModel
from .settings import ModelSettings


def _get_content_type(
    inp: RequestInput, inp_metadata: Optional[MetadataTensor]
) -> Optional[str]:
    if inp.parameters and inp.parameters.content_type:
        return inp.parameters.content_type

    if inp_metadata and inp_metadata.tags and inp_metadata.tags.content_type:
        return inp_metadata.tags.content_type

    return None


def _metadata_index(model_settings: ModelSettings) -> Dict[str, MetadataTensor]:
    index: Dict[str, MetadataTensor] = {}

    if not model_settings.inputs:
        return index

    for inp in model_settings.inputs:
        index[inp.name] = inp

    return index


def content_type_middleware(
    request: InferenceRequest, model: MLModel
) -> InferenceRequest:
    metadata_index = _metadata_index(model._settings)

    for inp in request.inputs:
        inp_metadata = metadata_index.get(inp.name)
        content_type = _get_content_type(inp, inp_metadata)
        if not content_type:
            continue

        codec = codecs.find_codec(content_type)
        decoded_payload = codec.decode(inp)

        if not inp.parameters:
            inp.parameters = Parameters()

        inp.parameters.decoded_content = decoded_payload  # type: ignore

    return request
