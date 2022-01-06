from typing import Dict

from grpc import ServicerContext


def to_headers(context: ServicerContext) -> Dict[str, str]:
    metadata = context.invocation_metadata() + context.trailing_metadata()
    headers = {}
    for metadatum in metadata:
        headers[metadatum.key] = metadatum.value

    return headers
