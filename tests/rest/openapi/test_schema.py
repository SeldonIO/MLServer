import pytest

from typing import Optional

from mlserver.rest.openapi.schema import (
    get_openapi_schema,
    get_model_schema,
    MODEL_VERSION_PARAMETER,
)


def test_get_openapi_schema():
    openapi_schema = get_openapi_schema()

    assert isinstance(openapi_schema, dict)
    assert "openapi" in openapi_schema


@pytest.mark.parametrize(
    "model_name, model_version",
    [
        ("sum-model", "v1.2.3"),
        ("sum-model", None),
    ],
)
def test_get_model_schema(model_name: str, model_version: Optional[str]):
    model_schema = get_model_schema(model_name, model_version)

    paths = model_schema["paths"]
    model_endpoint = f"/v2/models/{model_name}"
    if model_version:
        assert model_endpoint not in model_schema["paths"]
        assert f"{model_endpoint}/versions/{model_version}" in paths
    else:
        assert model_endpoint in model_schema["paths"]
        assert f"{model_endpoint}/versions/{{{MODEL_VERSION_PARAMETER}}}" in paths
