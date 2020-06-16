import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient
from mlserver.settings import Settings
from mlserver.rest import RESTServer


@pytest.fixture
def rest_settings() -> Settings:
    return Settings(debug=True)


@pytest.fixture
def rest_app(rest_settings, data_plane) -> FastAPI:
    server = RESTServer(rest_settings, data_plane)
    return server._app


@pytest.fixture
def rest_client(rest_app) -> TestClient:
    return TestClient(rest_app)
