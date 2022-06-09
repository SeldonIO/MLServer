import json

from pydantic import BaseModel
from typing import Dict, Tuple, List

try:
    import orjson
except ImportError:
    orjson = None  # type: ignore


def encode_value(v: BaseModel) -> str:
    as_dict = v.dict()
    if orjson is None:
        return json.dumps(as_dict)

    return orjson.dumps(as_dict)


def decode_value(v: bytes) -> dict:
    if orjson is None:
        return json.loads(v)

    return orjson.loads(v)


def encode_headers(h: Dict[str, str]) -> List[Tuple[str, bytes]]:
    return [(k, v.encode("utf-8")) for k, v in h.items()]


def decode_headers(h: List[Tuple[str, bytes]]) -> Dict[str, str]:
    return {k: v.decode("utf-8") for k, v in h}
