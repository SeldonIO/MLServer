from typing import Dict


def encode_headers(h: Dict[str, str]) -> Dict[str, str]:
    return {k: v.encode("utf-8") for k, v in request.headers}


def decode_headers(h: Dict[str, str]) -> Dict[str, str]:
    return {k: v.decode("utf-8") for k, v in request.headers}
