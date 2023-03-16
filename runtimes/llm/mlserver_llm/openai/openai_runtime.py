from typing import Any, Optional

import openai
import pandas as pd
from mlserver.codecs import StringCodec

from mlserver import ModelSettings
from mlserver.types import ResponseOutput
from .common import OpenAISettings, OpenAIModelTypeEnum
from .model_detail import get_openai_model_detail
from ..runtime import LLMRuntimeBase


class OpenAIRuntime(LLMRuntimeBase):
    """
    Runtime for OpenAI
    """

    def __init__(self, settings: ModelSettings):
        # if we are here we are sure that settings.parameters is set,
        # just helping mypy
        assert settings.parameters is not None
        assert settings.parameters.extra is not None
        config = settings.parameters.extra.config  # type: ignore
        self._openai_settings = OpenAISettings(**config)  # type: ignore
        self._model_dependency_reference = get_openai_model_detail(
            self._openai_settings.model_id)

        super().__init__(settings)

    async def load(self) -> bool:
        openai.api_key = self._openai_settings.api_key
        if self._openai_settings.organization:
            openai.organization = self._openai_settings.organization

        self.ready = True
        return self.ready

    async def _call_impl(
            self, input_data: Any, params: Optional[dict]) -> ResponseOutput:
        # TODO: make use of static parameters

        if self._model_dependency_reference.model_type == OpenAIModelTypeEnum.chat:
            result = await self._call_impl_chat(input_data, params)
            return StringCodec.encode_output(
                payload=[result], name="explanation"
            )
        raise TypeError(f"{self._model_dependency_reference.model_type} not supported")

    async def _call_impl_chat(
            self, input_data: Any, params: Optional[dict]) -> Any:
        assert isinstance(input_data, pd.DataFrame)
        return await openai.ChatCompletion.acreate(
            model=self._openai_settings.model_id,
            # TODO do df to list of messages
            messages=input_data.to_dict(),
            **params)


