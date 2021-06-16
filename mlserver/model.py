from typing import Any, Optional

from .types import (
    InferenceRequest,
    InferenceResponse,
    RequestInput,
    MetadataModelResponse,
)
from .settings import ModelSettings
from .codecs import DecodedParameterName, InputCodec


class MLModel:
    """
    Abstract class which serves as the main interface to interact with ML
    models.
    """

    def __init__(self, settings: ModelSettings):
        self._settings = settings
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

    def decode(
        self, request_input: RequestInput, default_codec: InputCodec = None
    ) -> Any:
        # NOTE: This method is now deprecated!
        # TODO: Remove once there aren't any references to self.decode()
        if request_input.parameters and hasattr(
            request_input.parameters, DecodedParameterName
        ):
            return getattr(request_input.parameters, DecodedParameterName)

        if default_codec:
            return default_codec.decode(request_input)

        return request_input.data

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
