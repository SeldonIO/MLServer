from fastapi import status
from typing import Optional


class MLServerError(Exception):
    def __init__(self, msg: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(msg)
        self.status_code = status_code


class InvalidModelURI(MLServerError):
    def __init__(self, name: str, model_uri: Optional[str] = None):
        msg = f"Invalid URI specified for model {name}"
        if model_uri:
            msg += f" ({model_uri})"

        super().__init__(msg, status.HTTP_422_UNPROCESSABLE_ENTITY)


class ModelNotFound(MLServerError):
    def __init__(self, name: str, version: Optional[str] = None):
        msg = f"Model {name} not found"
        if version is not None:
            msg = f"Model {name} with version {version} not found"

        super().__init__(msg, status.HTTP_404_NOT_FOUND)


class ModelNotReady(MLServerError):
    def __init__(self, name: str, version: Optional[str] = None):
        msg = f"Model {name} is not ready yet."
        if version is not None:
            msg = f"Model {name} with version {version} is not ready yet."

        super().__init__(msg, status.HTTP_400_BAD_REQUEST)


class InferenceError(MLServerError):
    def __init__(self, msg: str):
        super().__init__(msg, status.HTTP_400_BAD_REQUEST)


class ModelParametersMissing(MLServerError):
    def __init__(self, model_name: str):
        super().__init__(
            f"Parameters missing for model {model_name}", status.HTTP_400_BAD_REQUEST
        )
