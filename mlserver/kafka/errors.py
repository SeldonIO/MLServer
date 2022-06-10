from fastapi import status

from ..errors import MLServerError


class InvalidMessageHeaders(MLServerError):
    def __init__(self, missing_header: str):
        msg = (
            f"Invalid Kafka message. Expected '{missing_header}' header not "
            "found in message."
        )
        super().__init__(msg, status.HTTP_422_UNPROCESSABLE_ENTITY)
