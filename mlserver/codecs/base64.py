import base64

from typing import List

from ..types import RequestInput, ResponseOutput
from .base import InputCodec, register_input_codec
from .pack import pack, unpack, PackElement

_Base64StrCodec = "ascii"


def _to_bytes(elem: PackElement) -> bytes:
    if isinstance(elem, str):
        return elem.encode(_Base64StrCodec)

    # TODO: Ensure that payload is in base64
    return elem


@register_input_codec
class Base64Codec(InputCodec):
    """
    Encodes binary data as base64
    """

    ContentType = "base64"

    def encode(self, name: str, payload: List[bytes]) -> ResponseOutput:
        # Assume that payload is already in b64, so we only need to
        # pack it
        # TODO: Ensure that payload is in base64
        packed, shape = pack(payload)
        return ResponseOutput(
            name=name,
            datatype="BYTES",
            shape=shape,
            data=packed,
        )

    def decode(self, request_input: RequestInput) -> List[bytes]:
        packed = request_input.data.__root__
        shape = request_input.shape

        return list(map(_to_bytes, unpack(packed, shape)))
