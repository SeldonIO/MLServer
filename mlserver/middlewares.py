from .types import InferenceRequest
from .codecs import _codec_registry as codecs

ContentTypeKey = "content_type"
DecodedContentKey = "decoded_content"


def content_type_middleware(request: InferenceRequest) -> InferenceRequest:
    for inp in request.inputs:
        if not inp.parameters:
            continue

        if not inp.parameters.content_type:
            continue

        content_type = inp.parameters.content_type
        codec = codecs.find_codec(content_type)
        decoded_payload = codec.decode(inp)

        inp.parameters.decoded_content = decoded_payload  # type: ignore

    return request
