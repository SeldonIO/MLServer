from typing import Dict, Optional, List, Tuple

from pydantic import BaseModel
from ..codecs.json import encode_to_json_bytes, decode_from_bytelike_json_to_dict


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
        as_dict = value.model_dump()
        return KafkaMessage(key=key, value=as_dict, headers=headers)

    @classmethod
    def from_kafka_record(cls, kafka_record) -> "KafkaMessage":
        key = kafka_record.key
        value = decode_from_bytelike_json_to_dict(kafka_record.value)
        headers = _decode_headers(kafka_record.headers)
        return KafkaMessage(key=key, value=value, headers=headers)

    @property
    def encoded_key(self) -> bytes:
        if not self.key:
            return b""

        return self.key.encode("utf-8")

    @property
    def encoded_value(self) -> bytes:
        return encode_to_json_bytes(self.value)

    @property
    def encoded_headers(self) -> List[Tuple[str, bytes]]:
        return _encode_headers(self.headers)
