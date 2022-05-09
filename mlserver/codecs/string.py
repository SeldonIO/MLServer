from typing import Any, List

from ..types import RequestInput, ResponseOutput, Parameters

from .utils import SingleInputRequestCodec, is_list_of, InputOrOutput
from .base import InputCodec, register_input_codec, register_request_codec
from .pack import unpack, PackElement

_DefaultStrCodec = "utf-8"


def encode_str(elem: str) -> bytes:
    return elem.encode(_DefaultStrCodec)


def decode_str(encoded: PackElement, str_codec=_DefaultStrCodec) -> str:
    if encoded is None:
        return None
    if isinstance(encoded, bytes):
        return encoded.decode(str_codec)

    if isinstance(encoded, str):
        # NOTE: It may be a string already when decoded from json
        return encoded

    # TODO: Should we raise an error here?
    return ""


def _decode_input_or_output(input_or_output: InputOrOutput) -> List[str]:
    packed = input_or_output.data.__root__
    unpacked = map(decode_str, unpack(packed))
    return list(unpacked)


@register_input_codec
class StringCodec(InputCodec):
    """
    Encodes a Python string as a BYTES input.
    """

    ContentType = "str"

    @classmethod
    def can_encode(cls, payload: Any) -> bool:
        return is_list_of(payload, str)

    @classmethod
    def encode_output(cls, name: str, payload: List[str]) -> ResponseOutput:
        packed = map(encode_str, payload)
        shape = [len(payload)]
        return ResponseOutput(
            name=name,
            datatype="BYTES",
            shape=shape,
            data=list(packed),
            parameters=Parameters(content_type=cls.ContentType),
        )

    @classmethod
    def decode_output(cls, response_output: ResponseOutput) -> List[str]:
        return _decode_input_or_output(response_output)

    @classmethod
    def decode_input(cls, request_input: RequestInput) -> List[str]:
        return _decode_input_or_output(request_input)

    @classmethod
    def encode_input(cls, name: str, payload: List[str]) -> RequestInput:
        packed = map(encode_str, payload)
        shape = [len(payload)]
        return RequestInput(
            name=name,
            datatype="BYTES",
            shape=shape,
            data=list(packed),
            parameters=Parameters(content_type=cls.ContentType),
        )


@register_request_codec
class StringRequestCodec(SingleInputRequestCodec):
    InputCodec = StringCodec
    ContentType = StringCodec.ContentType
