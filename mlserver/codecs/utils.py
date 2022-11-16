from typing import Any, Union, Dict, Optional, List

from ..types import (
    InferenceRequest,
    InferenceResponse,
    RequestInput,
    RequestOutput,
    ResponseOutput,
    MetadataTensor,
    Parameters,
)
from ..settings import ModelSettings
from .base import (
    find_input_codec,
    find_input_codec_by_payload,
    find_request_codec,
    find_request_codec_by_payload,
    RequestCodec,
    InputCodecLike,
    RequestCodecLike,
)
from .errors import CodecError

DefaultOutputPrefix = "output-"
DefaultInputPrefix = "input-"

InputOrOutput = Union[RequestInput, ResponseOutput]
Codec = Union[InputCodecLike, RequestCodecLike]

Parametrised = Union[
    InferenceRequest, RequestInput, RequestOutput, ResponseOutput, InferenceResponse
]
Tagged = Union[MetadataTensor, ModelSettings]
DecodedParameterName = "_decoded_payload"


def inject_batch_dimension(shape: List[int]) -> List[int]:
    """
    Utility method to ensure that 1-dimensional shapes
    assume that `[N] == [N, D]`.
    """
    if len(shape) > 1:
        return shape

    return shape + [1]


def _get_content_type(
    request: Parametrised, metadata: Optional[Tagged] = None
) -> Optional[str]:
    if request.parameters and request.parameters.content_type:
        return request.parameters.content_type

    if metadata is not None:
        if metadata.parameters and metadata.parameters.content_type:
            return metadata.parameters.content_type

    return None


def _save_decoded(parametrised_obj: Parametrised, decoded_payload: Any):
    if not parametrised_obj.parameters:
        parametrised_obj.parameters = Parameters()

    setattr(parametrised_obj.parameters, DecodedParameterName, decoded_payload)


def encode_response_output(
    payload: Any,
    request_output: RequestOutput,
    metadata_outputs: Dict[str, MetadataTensor] = {},
) -> Optional[ResponseOutput]:
    output_metadata = metadata_outputs.get(request_output.name)
    content_type = _get_content_type(request_output, output_metadata)
    codec = (
        find_input_codec(content_type)
        if content_type
        else find_input_codec_by_payload(payload)
    )

    if not codec:
        return None

    return codec.encode_output(
        name=request_output.name,
        payload=payload,
    )


def encode_inference_response(
    payload: Any,
    model_settings: ModelSettings,
) -> Optional[InferenceResponse]:
    # TODO: Allow users to override codec through model's metadata
    codec = find_request_codec_by_payload(payload)

    if not codec:
        return None

    model_version = None
    if model_settings.parameters:
        model_version = model_settings.parameters.version

    return codec.encode_response(model_settings.name, payload, model_version)


def decode_request_input(
    request_input: RequestInput,
    metadata_inputs: Dict[str, MetadataTensor] = {},
) -> Optional[Any]:
    input_metadata = metadata_inputs.get(request_input.name)
    content_type = _get_content_type(request_input, input_metadata)
    if content_type is None:
        return None

    codec = find_input_codec(content_type)
    if codec is None:
        return None

    decoded_payload = codec.decode_input(request_input)
    _save_decoded(request_input, decoded_payload)
    return decoded_payload


def decode_inference_request(
    inference_request: InferenceRequest,
    model_settings: Optional[ModelSettings] = None,
    metadata_inputs: Dict[str, MetadataTensor] = {},
) -> Optional[Any]:
    for request_input in inference_request.inputs:
        decode_request_input(request_input, metadata_inputs)

    request_content_type = _get_content_type(inference_request, model_settings)
    if request_content_type is not None:
        codec = find_request_codec(request_content_type)
        if codec is not None:
            decoded_payload = codec.decode_request(inference_request)
            _save_decoded(inference_request, decoded_payload)
            return decoded_payload

    return inference_request


def has_decoded(parametrised_obj: Parametrised) -> bool:
    if parametrised_obj.parameters:
        return hasattr(parametrised_obj.parameters, DecodedParameterName)

    return False


def get_decoded(parametrised_obj: Parametrised) -> Any:
    if has_decoded(parametrised_obj):
        return getattr(parametrised_obj.parameters, DecodedParameterName)


def get_decoded_or_raw(parametrised_obj: Parametrised) -> Any:
    if not has_decoded(parametrised_obj):
        if isinstance(parametrised_obj, RequestInput):
            # If this is a RequestInput, return its data
            return parametrised_obj.data

        if isinstance(parametrised_obj, ResponseOutput):
            # If this is a ResponseOutput, return its data
            return parametrised_obj.data

        # Otherwise, return full object
        return parametrised_obj

    return get_decoded(parametrised_obj)


class SingleInputRequestCodec(RequestCodec):
    """
    The SingleInputRequestCodec can be used as a "meta-implementation" for other
    codecs. Its goal to decode the whole request simply as the first decoded
    element.
    """

    InputCodec: Optional[InputCodecLike] = None

    @classmethod
    def can_encode(cls, payload: Any) -> bool:
        if cls.InputCodec is None:
            return False

        return cls.InputCodec.can_encode(payload)

    @classmethod
    def encode_response(
        cls,
        model_name: str,
        payload: Any,
        model_version: Optional[str] = None,
        **kwargs,
    ) -> InferenceResponse:
        if cls.InputCodec is None:
            raise NotImplementedError(
                f"No input codec found for {type(cls)} request codec"
            )

        output = cls.InputCodec.encode_output(
            f"{DefaultOutputPrefix}1", payload, **kwargs
        )
        return InferenceResponse(
            model_name=model_name, model_version=model_version, outputs=[output]
        )

    @classmethod
    def decode_response(cls, response: InferenceResponse) -> Any:
        if len(response.outputs) != 1:
            raise CodecError(
                f"The '{cls.ContentType}' codec only supports a single output tensor "
                f"({len(response.outputs)} were received)"
            )

        first_output = response.outputs[0]
        if not has_decoded(first_output) and cls.InputCodec is not None:
            decoded_payload = cls.InputCodec.decode_output(first_output)  # type: ignore
            _save_decoded(first_output, decoded_payload)

        return get_decoded_or_raw(first_output)

    @classmethod
    def encode_request(cls, payload: Any, **kwargs) -> InferenceRequest:
        if cls.InputCodec is None:
            raise NotImplementedError(
                f"No input codec found for {type(cls)} request codec"
            )

        inp = cls.InputCodec.encode_input(f"{DefaultInputPrefix}1", payload, **kwargs)
        return InferenceRequest(inputs=[inp])

    @classmethod
    def decode_request(cls, request: InferenceRequest) -> Any:
        if len(request.inputs) != 1:
            raise CodecError(
                f"The '{cls.ContentType}' codec only supports a single input tensor "
                f"({len(request.inputs)} were received)"
            )

        first_input = request.inputs[0]
        if not has_decoded(first_input) and cls.InputCodec is not None:
            decoded_payload = cls.InputCodec.decode_input(first_input)  # type: ignore
            _save_decoded(first_input, decoded_payload)

        return get_decoded_or_raw(first_input)
