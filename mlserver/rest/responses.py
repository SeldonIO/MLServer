from fastapi.responses import ORJSONResponse as _ORJSONResponse
from starlette.responses import JSONResponse as _JSONResponse

try:
    import orjson
except ImportError:
    orjson = None

Response = _JSONResponse if orjson is None else _ORJSONResponse
