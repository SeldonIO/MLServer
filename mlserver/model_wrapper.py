from typing import Optional, List, Any

from mlserver.codecs import InputCodecLike, RequestCodecLike

from mlserver import MLModel, ModelSettings
from mlserver.types import (
    MetadataTensor,
    RequestInput,
    InferenceRequest,
    MetadataModelResponse,
    InferenceResponse,
)


class WrapperMLModel(MLModel):
    """Wrapper / Factory class for specific llm providers"""

    def __init__(self, settings: ModelSettings):
        self._rt = MLModel(settings)

    @property
    def name(self) -> str:
        return self._rt.name

    @property
    def version(self) -> Optional[str]:
        return self._rt.version

    @property
    def settings(self) -> ModelSettings:
        return self._rt.settings

    @property
    def inputs(self) -> Optional[List[MetadataTensor]]:
        return self._rt.inputs

    @inputs.setter
    def inputs(self, value: List[MetadataTensor]):
        self._rt.inputs = value

    @property
    def outputs(self) -> Optional[List[MetadataTensor]]:
        return self._rt.outputs

    @outputs.setter
    def outputs(self, value: List[MetadataTensor]):
        self._rt.outputs = value

    @property  # type: ignore
    def ready(self) -> bool:  # type: ignore
        return self._rt.ready

    @ready.setter
    def ready(self, value: bool):
        self._rt.ready = value

    def decode(
        self,
        request_input: RequestInput,
        default_codec: Optional[InputCodecLike] = None,
    ) -> Any:
        return self._rt.decode(request_input, default_codec)

    def decode_request(
        self,
        inference_request: InferenceRequest,
        default_codec: Optional[RequestCodecLike] = None,
    ) -> Any:
        return self._rt.decode_request(inference_request, default_codec)

    async def metadata(self) -> MetadataModelResponse:
        return await self._rt.metadata()

    async def load(self) -> bool:
        return await self._rt.load()

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        return await self._rt.predict(payload)
