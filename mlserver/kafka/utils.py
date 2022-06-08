from typing import Dict


def encode_headers(h: Dict[str, str]) -> Dict[str, bytes]:
    return {k: v.encode("utf-8") for k, v in h.items()}


def decode_headers(h: Dict[str, bytes]) -> Dict[str, str]:
    return {k: v.decode("utf-8") for k, v in h.items()}
