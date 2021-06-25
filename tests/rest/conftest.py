import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from mlserver.handlers import DataPlane, ModelRepositoryHandlers
from mlserver.rest import RESTServer
from mlserver import Settings

from ..fixtures import SumModel


@pytest.fixture
async def rest_server(
    settings: Settings,
    data_plane: DataPlane,
    model_repository_handlers: ModelRepositoryHandlers,
    sum_model: SumModel,
) -> RESTServer:
    server = RESTServer(
        settings,
        data_plane=data_plane,
        model_repository_handlers=model_repository_handlers,
    )

    await server.add_custom_handlers(sum_model)

    return server


@pytest.fixture
def rest_app(rest_server: RESTServer) -> FastAPI:
    return rest_server._app


@pytest.fixture
def rest_client(rest_app: FastAPI) -> TestClient:
    return TestClient(rest_app)
