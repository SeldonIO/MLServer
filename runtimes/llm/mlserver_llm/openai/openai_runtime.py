import json
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
        config = settings.parameters.extra['config']  # type: ignore
        self._openai_settings = OpenAISettings(**config)  # type: ignore
        self._model_dependency_reference = get_openai_model_detail(
            self._openai_settings.model_id)
        self._api_key = self._openai_settings.api_key
        self._organization = self._openai_settings.organization

        super().__init__(settings)

    async def _call_impl(
            self, input_data: Any, params: Optional[dict]) -> ResponseOutput:
        # TODO: make use of static parameters

        if self._model_dependency_reference.model_type == OpenAIModelTypeEnum.chat:
            result = await self._call_chat_impl(input_data, params)
            json_str = json.dumps(result)
            return StringCodec.encode_output(
                payload=[json_str], name="output"
            )
        raise TypeError(f"{self._model_dependency_reference.model_type} not supported")

    async def _call_chat_impl(
            self, input_data: Any, params: Optional[dict]) -> dict:
        assert isinstance(input_data, pd.DataFrame)
        data = _df_to_messages(input_data)
        return await openai.ChatCompletion.acreate(
            api_key=self._api_key,
            organization=self._organization,
            model=self._openai_settings.model_id,
            messages=data,
            **params)


def _df_to_messages(df: pd.DataFrame) -> list[dict]:
    assert 'role' in df.columns, 'user field not present'
    assert 'content' in df.columns, 'content field not present'
    return df[['role', 'content']].to_dict(orient='records')
