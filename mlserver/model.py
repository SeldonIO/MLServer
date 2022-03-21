from typing import Any, Dict, Optional, List

from .codecs import (
    encode_response_output,
    encode_inference_response,
    decode_request_input,
    decode_inference_request,
    has_decoded,
    get_decoded,
    InputCodecLike,
    RequestCodecLike,
)
from .codecs.errors import CodecNotFound
from .settings import ModelSettings
from .types import (
    InferenceRequest,
    InferenceResponse,
    RequestInput,
    RequestOutput,
    ResponseOutput,
    MetadataModelResponse,
    MetadataTensor,
)
from .types import (
    Parameters,
)


def _generate_metadata_index(
    metadata_tensors: Optional[List[MetadataTensor]],
) -> Dict[str, MetadataTensor]:
    metadata_index: Dict[str, MetadataTensor] = {}

    if not metadata_tensors:
        return metadata_index

    for metadata_tensor in metadata_tensors:
        metadata_index[metadata_tensor.name] = metadata_tensor

    return metadata_index


class MLModel:
    """
    Abstract class which serves as the main interface to interact with ML
    models.
    """

    def __init__(self, settings: ModelSettings):
        self._settings = settings
        self._inputs_index: Dict[str, MetadataTensor] = {}

        self._inputs_index = _generate_metadata_index(self._settings.inputs)
        self._outputs_index = _generate_metadata_index(self._settings.outputs)

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

    @property
    def settings(self) -> ModelSettings:
        return self._settings

    @property
    def inputs(self) -> Optional[List[MetadataTensor]]:
        return self._settings.inputs

    @inputs.setter
    def inputs(self, value: List[MetadataTensor]):
        self._settings.inputs = value
        self._inputs_index = _generate_metadata_index(self._settings.inputs)

    @property
    def outputs(self) -> Optional[List[MetadataTensor]]:
        return self._settings.outputs

    @outputs.setter
    def outputs(self, value: List[MetadataTensor]):
        self._settings.outputs = value
        self._outputs_index = _generate_metadata_index(self._settings.outputs)

    def decode(
        self,
        request_input: RequestInput,
        default_codec: Optional[InputCodecLike] = None,
    ) -> Any:
        decode_request_input(request_input, self._inputs_index)

        if has_decoded(request_input):
            return get_decoded(request_input)

        if default_codec:
            return default_codec.decode(request_input)

        return request_input.data

    def decode_request(
        self,
        inference_request: InferenceRequest,
        default_codec: Optional[RequestCodecLike] = None,
    ) -> Any:
        decode_inference_request(inference_request, self._settings, self._inputs_index)

        if has_decoded(inference_request):
            return get_decoded(inference_request)

        if default_codec:
            return default_codec.decode(inference_request)

        return inference_request

    def encode_response(
        self,
        payload: Any,
        default_codec: Optional[RequestCodecLike] = None,
    ) -> InferenceResponse:
        inference_response = encode_inference_response(payload, self._settings)

        if inference_response:
            return inference_response

        if default_codec:
            return default_codec.encode(self.name, payload, self.version)

        payload_type = str(type(payload))
        raise CodecNotFound(payload_type=payload_type, is_input=False, is_request=True)

    def encode(
        self,
        payload: Any,
        request_output: RequestOutput,
        default_codec: Optional[InputCodecLike] = None,
    ) -> ResponseOutput:
        response_output = encode_response_output(
            payload, request_output, self._outputs_index
        )

        if response_output:
            return response_output

        if default_codec:
            return default_codec.encode(request_output.name, payload)

        raise CodecNotFound(name=request_output.name, is_input=False, is_request=False)

    async def metadata(self) -> MetadataModelResponse:
        model_metadata = MetadataModelResponse(
            name=self.name,
            platform=self._settings.platform,
            versions=self._settings.versions,
            inputs=self._settings.inputs,
            outputs=self._settings.outputs,
        )

        if self._settings.parameters:
            model_metadata.parameters = Parameters(
                content_type=self._settings.parameters.content_type
            )

        return model_metadata

    async def load(self) -> bool:
        self.ready = True
        return self.ready

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        raise NotImplementedError("predict() method not implemented")
