import pytest

from mlflow.version import VERSION


@pytest.mark.parametrize("endpoint", ["/ping", "/health"])
async def test_ping(rest_client, endpoint: str):
    response = await rest_client.get(endpoint)

    assert response.status_code == 200
    assert response.json() == "\n"


async def test_version(rest_client):
    response = await rest_client.get("/version")

    assert response.status_code == 200
    assert response.json() == VERSION
