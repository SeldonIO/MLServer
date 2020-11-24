import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient
from mlserver.handlers import DataPlane, ModelRepositoryHandlers
from mlserver.rest import RESTServer
from mlserver import Settings


@pytest.fixture
def rest_app(
    settings: Settings,
    data_plane: DataPlane,
    model_repository_handlers: ModelRepositoryHandlers,
) -> FastAPI:
    server = RESTServer(
        settings,
        data_plane=data_plane,
        model_repository_handlers=model_repository_handlers,
    )
    return server._app


@pytest.fixture
def rest_client(rest_app: FastAPI) -> TestClient:
    return TestClient(rest_app)
