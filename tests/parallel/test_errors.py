import pytest

from fastapi import status
from asyncio import CancelledError

from mlserver.errors import MLServerError, ModelNotFound
from mlserver.parallel.errors import WorkerError


class CustomError(MLServerError):
    def __init__(self):
        super().__init__("foo")


@pytest.mark.parametrize(
    "exc, message, status_code",
    [
        (
            CustomError(),
            "tests.parallel.test_errors.CustomError: foo",
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            ModelNotFound("sum-model"),
            "mlserver.errors.ModelNotFound: Model sum-model not found",
            status.HTTP_404_NOT_FOUND,
        ),
        (
            Exception("bar"),
            "builtins.Exception: bar",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        ),
        (
            CancelledError("bad error"),
            "asyncio.exceptions.CancelledError: bad error",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        ),
    ],
)
def test_worker_error(exc, message, status_code):
    err = WorkerError(exc)

    assert str(err) == message
    assert err.status_code == status_code
