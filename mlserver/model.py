from typing import Any, Dict, Optional

from .types import (
    InferenceRequest,
    InferenceResponse,
    RequestInput,
    MetadataModelResponse,
    MetadataTensor,
)
from .settings import ModelSettings
from .codecs import (
    decode_request_input,
    decode_inference_request,
    InputCodec,
    has_decoded,
    get_decoded,
)


class MLModel:
    """
    Abstract class which serves as the main interface to interact with ML
    models.
    """

    def __init__(self, settings: ModelSettings):
        self._settings = settings
        self._inputs_index: Dict[str, MetadataTensor] = {}

        if self._settings.inputs:
            for request_input in self._settings.inputs:
                self._inputs_index[request_input.name] = request_input

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

    @property
    def settings(self) -> ModelSettings:
        return self._settings

    def decode(
        self, request_input: RequestInput, default_codec: Optional[InputCodec] = None
    ) -> Any:
        decode_request_input(request_input, self._inputs_index)

        if has_decoded(request_input):
            return get_decoded(request_input)

        if default_codec:
            return default_codec.decode(request_input)

        return request_input.data

    def decode_request(self, inference_request: InferenceRequest) -> Any:
        return decode_inference_request(inference_request, self._inputs_index)

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
