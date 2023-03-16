from typing import Any, Optional, List

from mlserver.codecs import (
    InputCodecLike,
    RequestCodecLike, PandasCodec,
)
from mlserver.model import MLModel
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

    def __init__(
        self, settings: ModelSettings, llm_settings: LLMSettings
    ):
        self.llm_settings = llm_settings
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


class LLMRuntime(MLModel):
    """Wrapper / Factory class for specific llm providers"""

    def __init__(self, settings: ModelSettings):
        assert settings.parameters is not None
        assert PROVIDER_ID_TAG in settings.parameters.extra  # type: ignore

        provider_id = settings.parameters.extra[PROVIDER_ID_TAG]  # type: ignore

        rt_class = import_and_get_class(get_mlmodel_class_as_str(provider_id))

        self._rt = rt_class(settings)

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

