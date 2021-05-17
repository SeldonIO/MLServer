from .types import InferenceRequest
from .codecs import _codec_registry as codecs

ContentTypeKey = "content_type"
DecodedContentKey = "decoded_content"


def content_type_middleware(request: InferenceRequest) -> InferenceRequest:
    for inp in request.inputs:
        if not inp.parameters:
            continue

        params = inp.parameters
        if not isinstance(params, dict):
            continue

        if ContentTypeKey not in params:
            continue

        content_type = params[ContentTypeKey]
        codec = codecs.find_codec(content_type)
        decoded_payload = codec.decode(inp)

        params[DecodedContentKey] = decoded_payload

    return request
