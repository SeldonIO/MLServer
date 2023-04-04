from mlserver.rest.docs import get_openapi_schema


def test_get_openapi_schema():
    openapi_schema = get_openapi_schema()

    assert isinstance(openapi_schema, dict)
    assert "openapi" in openapi_schema
