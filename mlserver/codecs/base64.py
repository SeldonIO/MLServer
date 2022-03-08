import base64
import binascii

from typing import Any, List

from ..types import RequestInput, ResponseOutput
from .utils import is_list_of
from .base import InputCodec, register_input_codec
from .pack import unpack, PackElement

_Base64StrCodec = "ascii"


def _ensure_bytes(elem: PackElement) -> bytes:
    if isinstance(elem, str):
        return elem.encode(_Base64StrCodec)

    return elem


def _encode_base64(elem: PackElement) -> bytes:
    as_bytes = _ensure_bytes(elem)
    return base64.b64encode(as_bytes)


def _decode_base64(elem: PackElement) -> bytes:
    as_bytes = _ensure_bytes(elem)

    # Check that the input is valid base64.
    # Otherwise, convert into base64.
    try:
        return base64.b64decode(as_bytes, validate=True)
    except binascii.Error:
        return as_bytes


@register_input_codec
class Base64Codec(InputCodec):
    """
    Codec that convers to / from a base64 input.
    """

    ContentType = "base64"

    @classmethod
    def can_encode(cls, payload: Any) -> bool:
        return is_list_of(payload, bytes)

    @classmethod
    def encode(cls, name: str, payload: List[bytes]) -> ResponseOutput:
        # Assume that payload is already in b64, so we only need to pack it
        packed = map(_encode_base64, payload)
        shape = [len(payload)]
        return ResponseOutput(
            name=name,
            datatype="BYTES",
            shape=shape,
            data=list(packed),
        )

    @classmethod
    def decode(cls, request_input: RequestInput) -> List[bytes]:
        packed = request_input.data.__root__

        return list(map(_decode_base64, unpack(packed)))
