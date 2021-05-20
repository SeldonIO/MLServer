from typing import Any, Dict, Optional

from .types import (
    InferenceRequest,
    InferenceResponse,
    RequestInput,
    MetadataModelResponse,
    MetadataTensor,
)
from .settings import ModelSettings
from .codecs import Codec, _codec_registry as codecs


def _metadata_index(model_settings: ModelSettings) -> Dict[str, MetadataTensor]:
    index: Dict[str, MetadataTensor] = {}

    if not model_settings.inputs:
        return index

    for inp in model_settings.inputs:
        index[inp.name] = inp

    return index


def _get_content_type(
    request_input: RequestInput, input_metadata: Optional[MetadataTensor]
) -> Optional[str]:
    if request_input.parameters and request_input.parameters.content_type:
        return request_input.parameters.content_type

    if input_metadata and input_metadata.tags and input_metadata.tags.content_type:
        return input_metadata.tags.content_type

    return None


def _get_codec(
    content_type: Optional[str], default_codec: Codec = None
) -> Optional[Codec]:
    if not content_type:
        return default_codec

    return codecs.find_codec(content_type)


class MLModel:
    """
    Abstract class which serves as the main interface to interact with ML
    models.
    """

    def __init__(self, settings: ModelSettings):
        self._settings = settings
        self._metadata_inputs = _metadata_index(self._settings)
        self.ready = False

    @property
    def name(self) -> str:
        return self._settings.name

    @property
    def version(self) -> Optional[str]:
        params = self._settings.parameters
        if params is not None:
            return params.version
        return None

    def decode(self, request_input: RequestInput, default_codec: Codec = None) -> Any:
        input_metadata = self._metadata_inputs.get(request_input.name)
        content_type = _get_content_type(request_input, input_metadata)
        codec = _get_codec(content_type, default_codec)
        if codec is None:
            return request_input.data

        return codec.decode(request_input)

    async def metadata(self) -> MetadataModelResponse:
        return MetadataModelResponse(
            name=self.name,
            platform=self._settings.platform,
            versions=self._settings.versions,
            inputs=self._settings.inputs,
            outputs=self._settings.outputs,
        )

    async def load(self) -> bool:
        self.ready = True
        return self.ready

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        raise NotImplementedError("predict() method not implemented")
