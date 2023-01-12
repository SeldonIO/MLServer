import json
import asyncio
import numpy as np
import functools

from typing import Any, Optional, List, Dict

import pandas as pd
from alibi.api.interfaces import Explanation, Explainer
from alibi.saving import load_explainer
from concurrent.futures import ThreadPoolExecutor

from mlserver.codecs import (
    NumpyRequestCodec,
    InputCodecLike,
    StringCodec,
    RequestCodecLike,
)
from mlserver.errors import ModelParametersMissing
from mlserver.handlers import custom_handler
from mlserver.model import MLModel
from mlserver.rest.responses import Response
from mlserver.settings import ModelSettings, ModelParameters
from mlserver.types import (
    InferenceRequest,
    InferenceResponse,
    RequestInput,
    MetadataModelResponse,
    Parameters,
    MetadataTensor,
    ResponseOutput,
)
from mlserver.utils import get_model_uri

from mlserver_alibi_explain.alibi_dependency_reference import (
    get_mlmodel_class_as_str,
    get_alibi_class_as_str,
)
from mlserver_alibi_explain.common import (
    AlibiExplainSettings,
    import_and_get_class,
    EXPLAIN_PARAMETERS_TAG,
    EXPLAINER_TYPE_TAG,
)
from mlserver_alibi_explain.errors import InvalidExplanationShape


class AlibiExplainRuntimeBase(MLModel):
    """
    Base class for Alibi-Explain models
    """

    def __init__(
        self, settings: ModelSettings, explainer_settings: AlibiExplainSettings
    ):

        self.alibi_explain_settings = explainer_settings
        self._executor = ThreadPoolExecutor()
        super().__init__(settings)

    async def explain_v1_output(self, request: InferenceRequest) -> Response:
        """
        A custom endpoint to return explanation results in plain json format (no v2
        encoding) to keep backward compatibility of legacy downstream users.

        This does not work with multi-model serving as no reference to the model exists
        in the endpoint.
        """
        v2_response = await self.predict(request)

        if len(v2_response.outputs) != 1:
            raise InvalidExplanationShape(len(v2_response.outputs))

        output = v2_response.outputs[0]

        if output.shape not in ([1], [1, 1]):
            raise InvalidExplanationShape(output.shape)

        explanation = json.loads(output.data[0])

        return Response(content=explanation, media_type="application/json")

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        """
        This is actually a call to explain as we are treating
        an explainer model as MLModel
        """

        # TODO: convert and validate?
        input_data = self.decode_request(payload, default_codec=NumpyRequestCodec)
        if isinstance(input_data, pd.DataFrame):
            input_data = np.array(input_data)
        output_data = await self._async_explain_impl(input_data, payload.parameters)

        return InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            outputs=[output_data],
            parameters=Parameters(
                headers={
                    "x-seldon-alibi-type": "explanation",
                    "x-seldon-alibi-method": self.get_alibi_method(),
                }
            ),
        )

    def get_alibi_method(self) -> str:
        module: str = type(self._model).__module__  # type: ignore
        return module.split(".")[-1]

    async def _async_explain_impl(
        self, input_data: Any, settings: Optional[Parameters]
    ) -> ResponseOutput:
        explain_parameters = dict()
        if settings is not None:
            settings_dict = settings.dict()
            if EXPLAIN_PARAMETERS_TAG in settings_dict:
                explain_parameters = settings_dict[EXPLAIN_PARAMETERS_TAG]

        loop = asyncio.get_running_loop()
        explain_call = functools.partial(
            self._explain_impl,
            input_data=input_data,
            explain_parameters=explain_parameters,
        )
        explanation = await loop.run_in_executor(self._executor, explain_call)
        # TODO: Convert alibi-explain output to v2 protocol, for now we use to_json
        return StringCodec.encode_output(
            payload=[explanation.to_json()], name="explanation"
        )

    async def _load_from_uri(self, predictor: Any) -> Explainer:
        # load the model from disk
        # full model is passed as `predictor`
        # load the model from disk
        model_parameters: Optional[ModelParameters] = self.settings.parameters
        if model_parameters is None:
            raise ModelParametersMissing(self.name)
        absolute_uri = await get_model_uri(self.settings)
        return await self._load_explainer(path=absolute_uri, predictor=predictor)

    async def _load_explainer(self, path: str, predictor: Any) -> Explainer:
        loop = asyncio.get_running_loop()
        load_call = functools.partial(load_explainer, path=path, predictor=predictor)
        return await loop.run_in_executor(self._executor, load_call)

    def _explain_impl(self, input_data: Any, explain_parameters: Dict) -> Explanation:
        """Actual explain to be implemented by subclasses"""
        raise NotImplementedError


class AlibiExplainRuntime(MLModel):
    """Wrapper / Factory class for specific alibi explain runtimes"""

    def __init__(self, settings: ModelSettings):
        # TODO: we probably want to validate the enum more sanely here
        # we do not want to construct a specific alibi settings here because
        # it might be dependent on type
        # although at the moment we only have one `AlibiExplainSettings`
        assert settings.parameters is not None
        assert EXPLAINER_TYPE_TAG in settings.parameters.extra  # type: ignore

        explainer_type = settings.parameters.extra[EXPLAINER_TYPE_TAG]  # type: ignore

        rt_class = import_and_get_class(get_mlmodel_class_as_str(explainer_type))

        alibi_class = import_and_get_class(get_alibi_class_as_str(explainer_type))

        self._rt = rt_class(settings, alibi_class)

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

    # we add _explain_v1_output here to enable the registration and routing of custom
    # endpoint to `_rt.explain_v1_output`
    @custom_handler(rest_path="/explain")
    async def _explain_v1_output(self, request: InferenceRequest) -> Response:
        return await self._rt.explain_v1_output(request)
