from typing import Optional
from fastapi import Request, status
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel

from ..errors import MLServerError


class APIErrorResponse(BaseModel):
    error: Optional[str] = None


def handle_mlserver_error(request: Request, exc: MLServerError) -> ORJSONResponse:
    err_res = APIErrorResponse(error=str(exc))
    return ORJSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content=err_res.dict()
    )


_EXCEPTION_HANDLERS = {MLServerError: handle_mlserver_error}
