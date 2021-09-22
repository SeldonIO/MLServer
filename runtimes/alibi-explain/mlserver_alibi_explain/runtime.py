import abc
import asyncio
import json
from typing import Any

import orjson
from alibi.api.interfaces import Explanation
from fastapi import Request, Response
from pydantic import BaseSettings

from mlserver.codecs import NumpyCodec
from mlserver.errors import InferenceError
from mlserver.handlers import custom_handler
from mlserver.model import MLModel
from mlserver.settings import ModelSettings
from mlserver.types import InferenceRequest, InferenceResponse
from mlserver_alibi_explain.common import create_v2_from_any


class AlibiExplainRuntimeBase(abc.ABC, MLModel):
    """
    Base class for Alibi-Explain models
    """

    def __init__(self, settings: ModelSettings, explainer_settings: BaseSettings):

        self.alibi_explain_settings = explainer_settings
        super().__init__(settings)

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:

        # TODO: convert and validate
        model_input = payload.inputs[0]
        default_codec = NumpyCodec()
        input_data = self.decode(model_input, default_codec=default_codec)
        explanation_dict = await self._async_explain_impl(input_data)

        # TODO: Convert alibi-explain output to v2 protocol, for now we use to_json
        output_data = explanation_dict

        return InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            outputs=[output_data],
        )

    @abc.abstractmethod
    def _infer_impl(self, input_data: Any) -> dict:
        """Implementers? or wrappers?"""

    @abc.abstractmethod
    def _explain_impl(self, input_data: Any) -> Explanation:
        """Actual explain fn"""

    async def _async_infer_impl(self, input_data: Any) -> dict:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._infer_impl, input_data)

    async def _async_explain_impl(self, input_data: Any) -> dict:
        loop = asyncio.get_event_loop()
        explanation = await loop.run_in_executor(None, self._explain_impl, input_data)
        return create_v2_from_any(explanation.to_json(), name="explain")


