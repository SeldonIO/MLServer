import abc
import asyncio
import json
from typing import Any, Union, List
import numpy as np

import orjson
from alibi.api.interfaces import Explanation
from fastapi import Request, Response
from pydantic import BaseSettings

from mlserver.codecs import NumpyCodec
from mlserver.errors import InferenceError
from mlserver.handlers import custom_handler
from mlserver.model import MLModel
from mlserver.settings import ModelSettings
from mlserver.types import InferenceRequest, InferenceResponse, Parameters, RequestInput
from mlserver_alibi_explain.common import create_v2_from_any, execute_async, remote_predict, AlibiExplainSettings


class AlibiExplainRuntimeBase(abc.ABC, MLModel):
    """
    Base class for Alibi-Explain models
    """

    def __init__(self, settings: ModelSettings, explainer_settings: AlibiExplainSettings):

        self.alibi_explain_settings = explainer_settings
        super().__init__(settings)

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        """This is actually a call to explain as we are treating an explainer model as MLModel"""

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

    def _infer_impl(self, input_data: Union[np.ndarray, List]) -> np.ndarray:
        # for now we only support v2 protocol
        # maybe also get the metadata and confirm / reshape types?
        # should mlflow codec do that?
        np_codec = NumpyCodec()

        # TODO: get it from codec? which explainer sends a list?
        if isinstance(input_data, list):
            input_data = np.array(input_data)

        # TODO: fixme as the reshape is required for mnist models
        num_samples = input_data.shape[0]
        input_data = input_data.reshape((num_samples, 1, -1))

        v2_request = InferenceRequest(
            parameters=Parameters(content_type=NumpyCodec.ContentType),
            inputs=[
                RequestInput(
                    name="predict",
                    shape=input_data.shape,
                    data=input_data.tolist(),  # we convert list above to np!
                    datatype="FP32",  # TODO: fixme as it will not work for anything!
                )
            ],
        )

        v2_response = remote_predict(
            v2_payload=v2_request,
            # TODO: get it from settings
            predictor_url=self.alibi_explain_settings.infer_uri)

        return np_codec.decode(v2_response.outputs[0])  # type: ignore # TODO: fix mypy and first output

    @abc.abstractmethod
    def _explain_impl(self, input_data: Any) -> Explanation:
        """Actual explain to be implemented by subclasses?"""

    async def _async_explain_impl(self, input_data: Any) -> dict:
        """run async"""
        explanation = await execute_async(self._explain_impl, input_data)
        return create_v2_from_any(explanation.to_json(), name="explain")


