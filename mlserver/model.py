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
    Abstract inference runtime which exposes the main interface to interact
    with ML models.
    """

    def __init__(self, settings: ModelSettings):
        self._settings = settings
        self._inputs_index: Dict[str, MetadataTensor] = {}

        self._inputs_index = _generate_metadata_index(self._settings.inputs)
        self._outputs_index = _generate_metadata_index(self._settings.outputs)

        self.ready = False

    async def load(self) -> bool:
        """
        Method responsible for loading the model from a model artefact.
        This method will be called on each of the parallel workers (when
        :doc:`parallel inference </user-guide/parallel-inference>`) is
        enabled).
        Its return value will represent the model's readiness status.
        A return value of ``True`` will mean the model is ready.

        **This method should be overriden to implement your custom load
        logic.**
        """
        return True

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        """
        Method responsible for running inference on the model.


        **This method should be overriden to implement your custom inference
        logic.**
        """
        raise NotImplementedError("predict() method not implemented")

    @property
    def name(self) -> str:
        """
        Model name, from the model settings.
        """
        return self._settings.name

    @property
    def version(self) -> Optional[str]:
        """
        Model version, from the model settings.
        """
        return self._settings.version

    @property
    def settings(self) -> ModelSettings:
        """
        Model settings.
        """
        return self._settings

    @property
    def inputs(self) -> Optional[List[MetadataTensor]]:
        """
        Expected model inputs, from the model settings.

        Note that this property can also be modified at model's load time to
        inject any inputs metadata.
        """
        return self._settings.inputs

    @inputs.setter
    def inputs(self, value: List[MetadataTensor]):
        self._settings.inputs = value
        self._inputs_index = _generate_metadata_index(self._settings.inputs)

    @property
    def outputs(self) -> Optional[List[MetadataTensor]]:
        """
        Expected model outputs, from the model settings.

        Note that this property can also be modified at model's load time to
        inject any outputs metadata.
        """
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
        """
        Helper to decode a **request input** into its corresponding high-level
        Python object.
        This method will find the most appropiate :doc:`input codec
        </user-guide/content-type>` based on the model's metadata and the
        input's content type.
        Otherwise, it will fall back to the codec specified in the
        ``default_codec`` kwarg.
        """
        decode_request_input(request_input, self._inputs_index)

        if has_decoded(request_input):
            return get_decoded(request_input)

        if default_codec:
            return default_codec.decode_input(request_input)

        return request_input.data

    def decode_request(
        self,
        inference_request: InferenceRequest,
        default_codec: Optional[RequestCodecLike] = None,
    ) -> Any:
        """
        Helper to decode an **inference request** into its corresponding
        high-level Python object.
        This method will find the most appropiate :doc:`request codec
        </user-guide/content-type>` based on the model's metadata and the
        requests's content type.
        Otherwise, it will fall back to the codec specified in the
        ``default_codec`` kwarg.
        """
        decode_inference_request(inference_request, self._settings, self._inputs_index)

        if has_decoded(inference_request):
            return get_decoded(inference_request)

        if default_codec:
            return default_codec.decode_request(inference_request)

        return inference_request

    def encode_response(
        self,
        payload: Any,
        default_codec: Optional[RequestCodecLike] = None,
    ) -> InferenceResponse:
        """
        Helper to encode a high-level Python object into its corresponding
        **inference response**.
        This method will find the most appropiate :doc:`request codec
        </user-guide/content-type>` based on the payload's type.
        Otherwise, it will fall back to the codec specified in the
        ``default_codec`` kwarg.
        """
        inference_response = encode_inference_response(payload, self._settings)

        if inference_response:
            return inference_response

        if default_codec:
            return default_codec.encode_response(self.name, payload, self.version)

        payload_type = str(type(payload))
        raise CodecNotFound(payload_type=payload_type, is_input=False, is_request=True)

    def encode(
        self,
        payload: Any,
        request_output: RequestOutput,
        default_codec: Optional[InputCodecLike] = None,
    ) -> ResponseOutput:
        """
        Helper to encode a high-level Python object into its corresponding
        **response output**.
        This method will find the most appropiate :doc:`input codec
        </user-guide/content-type>` based on the model's metadata, request
        output's content type or payload's type.
        Otherwise, it will fall back to the codec specified in the
        ``default_codec`` kwarg.
        """
        response_output = encode_response_output(
            payload, request_output, self._outputs_index
        )

        if response_output:
            return response_output

        if default_codec:
            return default_codec.encode_output(request_output.name, payload)

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
