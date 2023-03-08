from fastapi import status

from ..model import MLModel
from ..utils import get_import_path
from ..errors import MLServerError


class EnvironmentNotFound(MLServerError):
    def __init__(self, model: MLModel, env_hash: str):
        msg = (
            f"Environment with hash '{env_hash}' was not found for model '{model.name}'"
        )

        if model.version:
            msg += f" with version '{model.version}'"

        super().__init__(msg, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WorkerError(MLServerError):
    """
    Class used to wrap exceptions raised from the workers.

    All stacktrace details will be hidden, and the original class won't be
    returned. This is to avoid issues with custom exceptions, like:

        https://github.com/SeldonIO/MLServer/issues/881
    """

    def __init__(self, exc: BaseException):
        msg = str(exc)
        if isinstance(exc, BaseException):
            import_path = get_import_path(exc.__class__)
            msg = f"{import_path}: {exc}"

        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        if isinstance(exc, MLServerError):
            status_code = exc.status_code

        super().__init__(msg, status_code)
