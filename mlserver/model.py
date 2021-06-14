from typing import Any, Optional

from .types import (
    InferenceRequest,
    InferenceResponse,
    RequestInput,
    MetadataModelResponse,
)
from .settings import ModelSettings
from .codecs import DecodedParameterName


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

    def decode(self, request_input: RequestInput) -> Any:
        # TODO: Remove once there aren't any references to self.decode()
        if hasattr(request_input, DecodedParameterName):
            return getattr(request_input, DecodedParameterName)

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
