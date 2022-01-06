from typing import Dict, Tuple

from grpc import ServicerContext


def to_headers(context: ServicerContext) -> Dict[str, str]:
    metadata = context.invocation_metadata() + context.trailing_metadata()
    headers = {}
    for metadatum in metadata:
        headers[metadatum.key] = metadatum.value

    return headers


def to_metadata(headers: Dict[str, str]) -> Tuple[Tuple[str, str], ...]:
    return tuple(headers.items())
