from typing import Any, Union, List
from datetime import datetime

from ..types import RequestInput, ResponseOutput
from .utils import is_list_of
from .base import InputCodec, register_input_codec
from .pack import unpack, PackElement

_Datetime = Union[str, datetime]
_DatetimeStrCodec = "ascii"


def _to_iso(elem: _Datetime) -> str:
    if isinstance(elem, str):
        # Assume date has already been encoded upstream
        return elem

    return elem.isoformat()


def _encode_datetime(elem: _Datetime) -> bytes:
    iso_date = _to_iso(elem)
    return iso_date.encode(_DatetimeStrCodec)


def _ensure_str(elem: PackElement) -> str:
    if isinstance(elem, str):
        return elem

    return elem.decode(_DatetimeStrCodec)


def _decode_datetime(elem: PackElement) -> datetime:
    iso_format = _ensure_str(elem)
    return datetime.fromisoformat(iso_format)


@register_input_codec
class DatetimeCodec(InputCodec):
    """
    Codec that convers to / from a base64 input.
    """

    ContentType = "datetime"

    @classmethod
    def can_encode(cls, payload: Any) -> bool:
        return is_list_of(payload, datetime)

    @classmethod
    def encode(cls, name: str, payload: List[_Datetime]) -> ResponseOutput:
        packed = map(_encode_datetime, payload)
        shape = [len(payload)]
        return ResponseOutput(
            name=name,
            datatype="BYTES",
            shape=shape,
            data=list(packed),
        )

    @classmethod
    def decode(cls, request_input: RequestInput) -> List[datetime]:
        packed = request_input.data.__root__

        return list(map(_decode_datetime, unpack(packed)))
