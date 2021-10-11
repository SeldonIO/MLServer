from typing import Any, Optional, List

from alibi.api.interfaces import Explanation

from mlserver.codecs import NumpyCodec, InputCodec, StringCodec
from mlserver.model import MLModel
from mlserver.settings import ModelSettings
from mlserver.types import InferenceRequest, InferenceResponse, RequestInput, MetadataModelResponse, Parameters, \
    MetadataTensor, ResponseOutput
from mlserver_alibi_explain.common import execute_async, AlibiExplainSettings, \
    get_mlmodel_class_as_str, \
    get_alibi_class_as_str, import_and_get_class, EXPLAIN_PARAMETERS_TAG, EXPLAINER_TYPE_TAG


class AlibiExplainRuntimeBase(MLModel):
    """
    Base class for Alibi-Explain models
    """

    def __init__(self, settings: ModelSettings, explainer_settings: AlibiExplainSettings):

        self.alibi_explain_settings = explainer_settings
        super().__init__(settings)

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        """This is actually a call to explain as we are treating an explainer model as MLModel"""

        # TODO: convert and validate?
        model_input = payload.inputs[0]
        default_codec = NumpyCodec()
        input_data = self.decode(model_input, default_codec=default_codec)
        output_data = await self._async_explain_impl(input_data, payload.parameters)

        return InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            outputs=[output_data],
        )

    async def _async_explain_impl(self, input_data: Any, settings: Parameters) -> ResponseOutput:
        """run async"""
        explain_parameters = dict()
        if EXPLAIN_PARAMETERS_TAG in settings:
            explain_parameters = settings[EXPLAIN_PARAMETERS_TAG]

        explanation = await execute_async(
            loop=None,
            fn=self._explain_impl,
            input_data=input_data,
            explain_parameters=explain_parameters
        )
        # TODO: Convert alibi-explain output to v2 protocol, for now we use to_json
        return StringCodec.encode(payload=[explanation.to_json()], name="explain")

    def _explain_impl(self, input_data: Any, settings: Parameters) -> Explanation:
        """Actual explain to be implemented by subclasses"""
        raise NotImplementedError


class AlibiExplainRuntime(MLModel):
    """Wrapper / Factory class for specific alibi explain runtimes"""

    def __init__(self, settings: ModelSettings):
        # TODO: we probably want to validate the enum more sanely here
        # we do not want to construct a specific alibi settings here because it might be dependent on type
        # although at the moment we only have one `AlibiExplainSettings`
        explainer_type = settings.parameters.extra[EXPLAINER_TYPE_TAG]

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

    @property
    def ready(self) -> bool:
        return self._rt.ready

    @ready.setter
    def ready(self, value: bool):
        self._rt.ready = value

    def decode(
            self, request_input: RequestInput, default_codec: Optional[InputCodec] = None
    ) -> Any:
        return self._rt.decode(request_input, default_codec)

    def decode_request(self, inference_request: InferenceRequest) -> Any:
        return self._rt.decode_request(inference_request)

    async def metadata(self) -> MetadataModelResponse:
        return await self._rt.metadata()

    async def load(self) -> bool:
        return await self._rt.load()

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        return await self._rt.predict(payload)




