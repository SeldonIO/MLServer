from typing import Any, Union, Dict, Optional, Type

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
    InputCodec,
    RequestCodec,
)
from .errors import CodecError

DefaultOutputPrefix = "output-"

InputCodecLike = Union[Type[InputCodec], InputCodec]
RequestCodecLike = Union[Type[RequestCodec], RequestCodec]

Parametrised = Union[InferenceRequest, RequestInput, RequestOutput]
Tagged = Union[MetadataTensor, ModelSettings]
DecodedParameterName = "_decoded_payload"


def is_list_of(payload: Any, instance_type: Type):
    if not isinstance(payload, list):
        return False

    def isinstance_of_type(payload: Any) -> bool:
        return isinstance(payload, instance_type)

    return all(map(isinstance_of_type, payload))


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

    return codec.encode(
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

    return codec.encode(model_settings.name, payload, model_version)


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

    decoded_payload = codec.decode(request_input)
    _save_decoded(request_input, decoded_payload)
    return decoded_payload


def decode_inference_request(
    inference_request: InferenceRequest,
    model_settings: ModelSettings = None,
    metadata_inputs: Dict[str, MetadataTensor] = {},
) -> Optional[Any]:
    for request_input in inference_request.inputs:
        decode_request_input(request_input, metadata_inputs)

    request_content_type = _get_content_type(inference_request, model_settings)
    if request_content_type is not None:
        codec = find_request_codec(request_content_type)
        if codec is not None:
            decoded_payload = codec.decode(inference_request)
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

        # Otherwise, return full object
        return parametrised_obj

    return get_decoded(parametrised_obj)


class SingleInputRequestCodec(RequestCodec):
    """
    The SingleInputRequestCodec can be used as a "meta-implementation" for other
    codecs. Its goal to decode the whole request simply as the first decoded
    element.
    """

    InputCodec: Optional[Type[InputCodec]] = None

    @classmethod
    def can_encode(cls, payload: Any) -> bool:
        if cls.InputCodec is None:
            return False

        return cls.InputCodec.can_encode(payload)

    @classmethod
    def encode(
        cls, model_name: str, payload: Any, model_version: str = None
    ) -> InferenceResponse:
        if cls.InputCodec is None:
            raise NotImplementedError(
                f"No input codec found for {type(cls)} request codec"
            )

        output = cls.InputCodec.encode(f"{DefaultOutputPrefix}1", payload)
        return InferenceResponse(
            model_name=model_name, model_version=model_version, outputs=[output]
        )

    @classmethod
    def decode(cls, request: InferenceRequest) -> Any:
        if len(request.inputs) != 1:
            raise CodecError(
                f"The '{cls.ContentType}' codec only supports a single input tensor "
                f"({len(request.inputs)} were received)"
            )

        first_input = request.inputs[0]
        if not has_decoded(first_input) and cls.InputCodec is not None:
            decoded_payload = cls.InputCodec.decode(first_input)  # type: ignore
            _save_decoded(first_input, decoded_payload)

        return get_decoded_or_raw(first_input)
