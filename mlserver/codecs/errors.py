from ..errors import MLServerError


class CodecNotFound(MLServerError):
    def __init__(
        self,
        name: str = None,
        payload_type: str = None,
        is_input: bool = False,
        is_request: bool = False,
    ):
        msg = ""
        if name:
            msg = f"with name {name}"

            if payload_type:
                msg = f"{msg} and type {payload_type}"
        elif payload_type:
            msg = f"with type {payload_type}"

        field_category = ""
        if is_input:
            if is_request:
                field_category = "input request"
            else:
                field_category = "input field"
        else:
            if is_request:
                field_category = "output response"
            else:
                field_category = "output field"

        msg = f"Codec not found for {field_category} {msg}"
        super().__init__(msg)


class CodecError(MLServerError):
    def __init__(self, msg: str):
        msg = f"There was an error encoding / decoding the payload: {msg}"
        super().__init__(msg)
