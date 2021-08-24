import base64

from typing import List

from ..types import RequestInput, ResponseOutput
from .base import InputCodec, register_input_codec
from .pack import pack, unpack, PackElement

_Base64StrCodec = "ascii"


def _decode_base64(elem: PackElement) -> bytes:
    as_bytes = elem.encode(_Base64StrCodec) if isinstance(elem, str) else elem
    return base64.b64decode(as_bytes)


@register_input_codec
class Base64Codec(InputCodec):
    """
    Encodes binary data as base64
    """

    ContentType = "base64"

    def encode(self, name: str, payload: List[bytes]) -> ResponseOutput:
        packed, shape = pack(map(base64.b64encode, payload))
        return ResponseOutput(
            name=name,
            datatype="BYTES",
            shape=shape,
            data=packed,
        )

    def decode(self, request_input: RequestInput) -> List[str]:
        packed = request_input.data.__root__
        shape = request_input.shape

        return map(_decode_base64, unpack(packed, shape))
