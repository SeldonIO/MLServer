from typing import Optional
from fastapi import Request
from pydantic import BaseModel

from .responses import Response
from ..errors import MLServerError


class APIErrorResponse(BaseModel):
    error: Optional[str] = None


async def handle_mlserver_error(request: Request, exc: MLServerError) -> Response:
    err_res = APIErrorResponse(error=str(exc))
    return Response(status_code=exc.status_code, content=err_res.dict())


_EXCEPTION_HANDLERS = {MLServerError: handle_mlserver_error}
