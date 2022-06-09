import json

from typing import Dict, Optional, List, Tuple, Union

from pydantic import BaseModel

try:
    import orjson
except ImportError:
    orjson = None  # type: ignore


def _encode_value(v: dict) -> bytes:
    if orjson is None:
        dumped = json.dumps(v)
        return dumped.encode("utf-8")

    return orjson.dumps(v)


def _decode_value(v: Union[bytes, str]) -> dict:
    if orjson is None:
        return json.loads(v)

    return orjson.loads(v)


def _encode_headers(h: Dict[str, str]) -> List[Tuple[str, bytes]]:
    return [(k, v.encode("utf-8")) for k, v in h.items()]


def _decode_headers(h: List[Tuple[str, bytes]]) -> Dict[str, str]:
    return {k: v.decode("utf-8") for k, v in h}


class KafkaMessage(BaseModel):
    key: Optional[str] = None
    value: dict
    headers: Dict[str, str]

    @classmethod
    def from_types(
        cls, key: Optional[str], value: BaseModel, headers: Dict[str, str]
    ) -> "KafkaMessage":
        as_dict = value.dict()
        return KafkaMessage(key=key, value=as_dict, headers=headers)

    @classmethod
    def from_kafka_record(cls, kafka_record) -> "KafkaMessage":
        key = kafka_record.key
        value = _decode_value(kafka_record.value)
        headers = _decode_headers(kafka_record.headers)
        return KafkaMessage(key=key, value=value, headers=headers)

    @property
    def encoded_key(self) -> bytes:
        if not self.key:
            return b""

        return self.key.encode("utf-8")

    @property
    def encoded_value(self) -> bytes:
        return _encode_value(self.value)

    @property
    def encoded_headers(self) -> List[Tuple[str, bytes]]:
        return _encode_headers(self.headers)
