from typing import Any

from starlette.responses import JSONResponse as _JSONResponse

from ..codecs.json import encode_to_json_bytes


class Response(_JSONResponse):
    """
    Custom Response that will use the encode_to_json_bytes function to
    encode given content to json based on library availability.
    See mlserver/codecs/utils.py for more details
    """

    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        return encode_to_json_bytes(content)
