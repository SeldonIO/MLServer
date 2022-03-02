from ..errors import MLServerError


class CodecNotFound(MLServerError):
    def __init__(self, name: str = None, payload_type: str = None):
        msg = ""
        if name:
            msg = f"with name {name}"

            if payload_type:
                msg = f"{msg} and type {payload_type}"

        if payload_type:
            msg = f"with type {payload_type}"

        msg = f"Codec not found for input / output {msg}"
        super().__init__(msg, status.HTTP_400_BAD_REQUEST)


class CodecError(MLServerError):
    def __init__(self, msg: str):
        super().__init__(f"There was an error encoding / decoding the payload: {msg}")
