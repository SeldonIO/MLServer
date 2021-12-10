from typing import List

from ..types import RequestInput, ResponseOutput, Parameters

from .utils import FirstInputRequestCodec
from .base import InputCodec, register_input_codec, register_request_codec
from .pack import unpack, PackElement

_DefaultStrCodec = "utf-8"


def encode_str(elem: str) -> bytes:
    return elem.encode(_DefaultStrCodec)


def decode_str(encoded: PackElement, str_codec=_DefaultStrCodec) -> str:
    if isinstance(encoded, bytes):
        return encoded.decode(str_codec)

    if isinstance(encoded, str):
        # NOTE: It may be a string already when decoded from json
        return encoded

    # TODO: Should we raise an error here?
    return ""


@register_input_codec
class StringCodec(InputCodec):
    """
    Encodes a Python string as a BYTES input.
    """

    ContentType = "str"

    @classmethod
    def encode(cls, name: str, payload: List[str]) -> ResponseOutput:
        packed = map(encode_str, payload)
        shape = [len(payload)]
        return ResponseOutput(
            name=name,
            datatype="BYTES",
            shape=shape,
            data=list(packed),
        )

    @classmethod
    def decode(cls, request_input: RequestInput) -> List[str]:
        packed = request_input.data.__root__

        unpacked = map(decode_str, unpack(packed))
        return list(unpacked)

    @classmethod
    def encode_request_input(cls, name: str, payload: List[str]) -> RequestInput:
        # TODO: merge this logic with `encode`
        # note: this will only work with REST and not grpc as we might have
        # variable length strings
        return RequestInput(
            name=name,
            datatype="BYTES",
            shape=[len(payload)],  # this is discarded downstream?
            data=payload,
            parameters=Parameters(content_type=cls.ContentType),
        )


@register_request_codec
class StringRequestCodec(FirstInputRequestCodec):
    InputCodec = StringCodec
    ContentType = StringCodec.ContentType
