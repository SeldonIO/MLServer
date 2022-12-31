from typing import Optional, Type, Any, Dict, List, Union, Sequence
from mlserver.codecs.utils import (
    has_decoded,
    _save_decoded,
    get_decoded_or_raw,
)
from mlserver.codecs import StringCodec
from mlserver.codecs.base import (
    RequestCodec,
    register_request_codec,
    InputCodec as InputCodecTy,
)
from mlserver.codecs.base import (
    find_input_codec,
    find_input_codec_by_payload,
)
from mlserver.types import (
    Parameters,
    InferenceRequest,
    InferenceResponse,
    RequestInput,
    ResponseOutput,
)
from .image import PILImageCodec
from .json import HuggingfaceSingleJSONCodec
from .jsonlist import HuggingfaceListJSONCodec
from .conversation import HuggingfaceConversationCodec
from .numpylist import NumpyListCodec
from .raw import RawCodec


def set_content_type(input_v: RequestInput, content_type: str):
    if input_v.parameters is None:
        input_v.parameters = Parameters(content_type=content_type)
        return
    if not input_v.parameters.content_type:
        input_v.parameters.content_type = content_type


class MultiInputRequestCodec(RequestCodec):
    """
    Huggingface codecs is prefered, then mlserver's
    """

    DefaultCodec: Type["InputCodecTy"] = StringCodec
    InputCodecsWithPriority: List[Type[InputCodecTy]] = []
    ContentType = StringCodec.ContentType

    @classmethod
    def _find_encode_codecs(
        cls, payload: Dict[str, Any]
    ) -> Dict[str, Union[Type["InputCodecTy"], "InputCodecTy", None]]:
        field_codec: Dict[str, Union[Type["InputCodecTy"], "InputCodecTy", None]] = {}
        for field, value in payload.items():
            for codec in cls.InputCodecsWithPriority:
                if codec.can_encode(value):
                    field_codec[field] = codec
                    break
            if field not in field_codec:
                field_codec[field] = find_input_codec_by_payload(value)

        return field_codec

    @classmethod
    def _find_decode_codecs(
        cls, data: Union[InferenceResponse, InferenceRequest]
    ) -> Dict[str, Union[Type[InputCodecTy], InputCodecTy, None]]:
        field_codec: Dict[str, Union[Type[InputCodecTy], InputCodecTy, None]] = {}
        default_codec: Union[Type[InputCodecTy], InputCodecTy, None] = None
        fields: Sequence[Union[RequestInput, ResponseOutput]] = []
        if data.parameters and data.parameters.content_type:
            default_codec = find_input_codec(data.parameters.content_type)
        if default_codec is None:
            default_codec = cls.DefaultCodec
        if isinstance(data, InferenceRequest):
            fields = data.inputs
        else:
            fields = data.outputs  # type: ignore
        for field in fields:
            if not field.parameters:
                field_codec[field.name] = default_codec
                continue
            if not field.parameters.content_type:
                field_codec[field.name] = default_codec
                continue
            codec = find_input_codec(field.parameters.content_type)
            if codec:
                field_codec[field.name] = codec
            else:
                field_codec[field.name] = default_codec
        return field_codec

    @classmethod
    def _can_encode_request(cls, payload: Dict[str, Any]) -> bool:
        field_codecs = cls._find_encode_codecs(payload)
        return bool(all(field_codecs.values()))

    @classmethod
    def can_encode(cls, payload: Dict[str, Any]) -> bool:
        """
        Inputs always is Dict, Outputs always is list
        """
        if isinstance(payload, dict):
            return cls._can_encode_request(payload)
        elif isinstance(payload, list):
            return True
        else:
            return False

    @classmethod
    def encode_response(
        cls,
        model_name: str,
        payload: List[Any],
        model_version: Optional[str] = None,
        **kwargs,
    ) -> InferenceResponse:
        """
        Always use HuggingfaceListJSONCodec
        """
        if not isinstance(payload, list):
            payload = [payload]
        return InferenceResponse(
            model_name=model_name,
            model_version=model_version,
            outputs=[HuggingfaceListJSONCodec.encode_output("output", payload)],
        )

    @classmethod
    def decode_response(
        cls, response: InferenceResponse
    ) -> Union[List[Any], Dict[Any, Any]]:
        data = {}
        is_list = True
        field_codecs = cls._find_decode_codecs(response)
        for item in response.outputs:
            if not has_decoded(item):
                codec = field_codecs[item.name]
                if codec is not None:
                    decoded_payload = codec.decode_output(item)
                    _save_decoded(item, decoded_payload)

            value = get_decoded_or_raw(item)
            data[item.name] = value
            if not item.name.startswith("output_"):
                is_list = False
        if not is_list:
            return data
        return [data[key] for key in sorted(data)]

    @classmethod
    def encode_request(cls, payload: Dict[str, Any], **kwargs) -> InferenceRequest:
        field_codecs = cls._find_encode_codecs(payload)
        inputs = []
        for key, value in payload.items():
            codec = field_codecs[key]
            if codec is None:
                raise Exception(
                    f"codec for key {key} value not found, value is {value}"
                )
            input_v = codec.encode_input(key, value, **kwargs)
            set_content_type(input_v, codec.ContentType)
            inputs.append(input_v)
        return InferenceRequest(
            parameters=Parameters(
                content_type=cls.ContentType,
            ),
            inputs=inputs,
        )

    @classmethod
    def decode_request(cls, request: InferenceRequest) -> Dict[str, Any]:
        values = {}
        field_codecs = cls._find_decode_codecs(request)
        for item in request.inputs:
            if not has_decoded(item):
                codec = field_codecs[item.name]
                if codec is not None:
                    decoded_payload = codec.decode_input(item)
                    _save_decoded(item, decoded_payload)

            value = get_decoded_or_raw(item)
            values[item.name] = value
        return values


@register_request_codec
class HuggingfaceRequestCodec(MultiInputRequestCodec):
    InputCodecsWithPriority = [
        PILImageCodec,
        HuggingfaceSingleJSONCodec,
        HuggingfaceListJSONCodec,
        HuggingfaceConversationCodec,
        NumpyListCodec,
        RawCodec,
    ]
    ContentType = StringCodec.ContentType
    DefaultCodec = StringCodec
