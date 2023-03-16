from typing import Any, Optional

import openai

from mlserver import ModelSettings
from mlserver.types import Parameters, ResponseOutput
from .common import OpenAISettings, OpenAIModelTypeEnum
from .dependency_reference import get_openai_model_dependency_detail
from ..dependency_reference import import_and_get_class
from ..runtime import LLMRuntimeBase


class OpenAIRuntime(LLMRuntimeBase):
    """
    Runtime for OpenAI
    """

    async def _call_impl(
            self, input_data: Any, params: Optional[dict]) -> ResponseOutput:
        # TODO: make use of static parameters

        if self._model_dependency_reference.model_type == OpenAIModelTypeEnum.chat:
            return await self._call_impl_chat(input_data, params)
        pass

    async def _call_impl_chat(
            self, input_data: Any, params: Optional[dict]) -> ResponseOutput:
        # TODO: how can we get mypy here?
        result = self._client.acreate(
            model=self._openai_settings.model_id, messages=input_data, **params)
        pass

    def __init__(self, settings: ModelSettings):
        # if we are here we are sure that settings.parameters is set,
        # just helping mypy
        assert settings.parameters is not None
        assert settings.parameters.extra is not None
        config = settings.parameters.extra.config  # type: ignore
        self._openai_settings = OpenAISettings(**config)  # type: ignore
        self._model_dependency_reference = get_openai_model_dependency_detail(
            self._openai_settings.model_id)
        self._client = import_and_get_class(self._model_dependency_reference.model_id)()

        super().__init__(settings)

