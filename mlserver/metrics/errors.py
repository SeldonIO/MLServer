from fastapi import status

from ..errors import MLServerError


class InvalidModelContext(MLServerError):
    def __init__(self):
        msg = (
            "Contextual method (e.g. mlserver.log() or mlserver.register())"
            " was called outside of a model context. "
        )
        super().__init__(msg, status.HTTP_500_INTERNAL_SERVER_ERROR)
