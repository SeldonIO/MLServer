import base64
import binascii

from typing import List

from ..types import RequestInput, ResponseOutput
from .base import InputCodec, register_input_codec
from .pack import pack, unpack, PackElement

_Base64StrCodec = "ascii"


def _ensure_bytes(elem: PackElement) -> bytes:
    if isinstance(elem, str):
        return elem.encode(_Base64StrCodec)

    return elem


def _ensure_base64(elem: PackElement) -> bytes:
    as_bytes = _ensure_bytes(elem)

    # Check that the input is valid base64.
    # Otherwise, convert into base64.
    try:
        base64.b64decode(as_bytes, validate=True)
        return as_bytes
    except binascii.Error:
        return base64.b64encode(as_bytes)


@register_input_codec
class Base64Codec(InputCodec):
    """
    Ensures that the input that the model receives is a base64 bytes array.
    """

    ContentType = "base64"

    def encode(self, name: str, payload: List[bytes]) -> ResponseOutput:
        # Assume that payload is already in b64, so we only need to pack it
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

        return list(map(_ensure_base64, unpack(packed, shape)))
