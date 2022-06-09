from typing import Dict, Tuple, List


def encode_headers(h: Dict[str, str]) -> List[Tuple[str, bytes]]:
    return [(k, v.encode("utf-8")) for k, v in h.items()]


def decode_headers(h: List[Tuple[str, bytes]]) -> Dict[str, str]:
    return {k: v.decode("utf-8") for k, v in h}
