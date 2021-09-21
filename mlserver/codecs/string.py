from typing import List

from ..types import RequestInput, ResponseOutput

from .utils import FirstInputRequestCodec
from .base import InputCodec, register_input_codec, register_request_codec
from .pack import pack, unpack, PackElement

_DefaultStrCodec = "utf-8"


def _encode_str(elem: str) -> bytes:
    return elem.encode(_DefaultStrCodec)


def _decode_str(encoded: PackElement, str_codec=_DefaultStrCodec) -> str:
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
        packed, shape = pack(map(_encode_str, payload))
        return ResponseOutput(
            name=name,
            datatype="BYTES",
            shape=shape,
            data=packed,
        )

    @classmethod
    def decode(cls, request_input: RequestInput) -> List[str]:
        packed = request_input.data.__root__
        shape = request_input.shape

        unpacked = map(_decode_str, unpack(packed, shape))
        return list(unpacked)


@register_request_codec
class StringRequestCodec(FirstInputRequestCodec):
    InputCodec = StringCodec
    ContentType = StringCodec.ContentType
