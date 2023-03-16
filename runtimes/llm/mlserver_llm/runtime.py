from typing import Any, Optional, List

from mlserver.codecs import (
    InputCodecLike,
    RequestCodecLike, PandasCodec,
)
from mlserver.model import MLModel
from mlserver.model_wrapper import WrapperMLModel
from mlserver.settings import ModelSettings
from mlserver.types import (
    InferenceRequest,
    InferenceResponse,
    RequestInput,
    MetadataModelResponse,
    MetadataTensor,
    ResponseOutput,
)
from .common import (
    LLMSettings, LLM_CALL_PARAMETERS_TAG
)
from .dependency_reference import get_mlmodel_class_as_str, import_and_get_class


class LLMRuntimeBase(MLModel):
    """
    Base class for LLM models hosted by a provider (e.g. OpenAI)
    """

    def __init__(self, settings: ModelSettings):
        super().__init__(settings)

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        """
        This will call the model endpoint for inference
        """

        # TODO: what are the better codecs for the different types of openai models?
        input_data = self.decode_request(payload, default_codec=PandasCodec)
        call_parameters = _get_predict_parameters(payload)
        # TODO: deal with error and retries
        output_data = await self._call_impl(input_data, call_parameters)

        return InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            outputs=[output_data],
        )

    async def _call_impl(
            self, input_data: Any, params: Optional[dict]) -> ResponseOutput:
        raise NotImplementedError


def _get_predict_parameters(payload: InferenceRequest) -> dict:
    runtime_parameters = dict()
    if payload.parameters is not None:
        settings_dict = payload.parameters.dict()
        if LLM_CALL_PARAMETERS_TAG in settings_dict:
            runtime_parameters = settings_dict[LLM_CALL_PARAMETERS_TAG]
    return runtime_parameters


class LLMRuntime(WrapperMLModel):
    """Wrapper / Factory class for specific llm providers"""

    def __init__(self, settings: ModelSettings):
        assert settings.parameters is not None
        assert PROVIDER_ID_TAG in settings.parameters.extra  # type: ignore

        provider_id = settings.parameters.extra[PROVIDER_ID_TAG]  # type: ignore

        rt_class = import_and_get_class(get_mlmodel_class_as_str(provider_id))

        self._rt = rt_class(settings)
