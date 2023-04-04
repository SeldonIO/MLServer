import orjson

from importlib_resources import files

OPENAPI_SCHEMA_RELATIVE_PATH = "../openapi/dataplane.json"


def get_openapi_schema() -> dict:
    mlserver_package = __package__.split(".")[0]
    openapi_schema_path = files(mlserver_package).joinpath(OPENAPI_SCHEMA_RELATIVE_PATH)
    return orjson.loads(openapi_schema_path.read_bytes())
