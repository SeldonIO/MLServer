from mlserver.errors import MLServerError
from typing import Optional


class InvalidMLlibFormat(MLServerError):
    def __init__(self, name: str, model_uri: Optional[str] = None):
        msg = f"Invalid MLlib format for model {name}"
        if model_uri:
            msg += f" ({model_uri})"

        super().__init__(msg)
