from typing import Any

from pydantic import BaseModel
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


class ServerSentEvent:
    def __init__(self, data: BaseModel, *args, **kwargs):
        # NOTE: SSE should use `\n\n` as separator
        # https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#event_stream_format
        self._sep = b"\n\n"
        self._pre = b"data: "
        self.data = data

    def encode(self) -> bytes:
        as_dict = self.data.model_dump()
        return self._pre + encode_to_json_bytes(as_dict) + self._sep