import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from mlserver.handlers import DataPlane, ModelRepositoryHandlers
from mlserver.registry import MultiModelRegistry
from mlserver.rest import RESTServer
from mlserver.repository import ModelRepository
from mlserver import Settings

from mlserver_mlflow import MLflowRuntime


@pytest.fixture
def model_repository(model_uri: str) -> ModelRepository:
    return ModelRepository(model_uri)


@pytest.fixture
async def model_registry(runtime: MLflowRuntime) -> MultiModelRegistry:
    model_registry = MultiModelRegistry()
    await model_registry.load(runtime)
    return model_registry


@pytest.fixture
def settings() -> Settings:
    return Settings()


@pytest.fixture
def data_plane(settings: Settings, model_registry: MultiModelRegistry) -> DataPlane:
    return DataPlane(settings=settings, model_registry=model_registry)


@pytest.fixture
def model_repository_handlers(
    model_repository: ModelRepository, model_registry: MultiModelRegistry
) -> ModelRepositoryHandlers:
    return ModelRepositoryHandlers(
        repository=model_repository, model_registry=model_registry
    )


@pytest.fixture
async def rest_server(
    settings: Settings,
    data_plane: DataPlane,
    model_repository_handlers: ModelRepositoryHandlers,
    runtime: MLflowRuntime,
) -> RESTServer:
    server = RESTServer(
        settings,
        data_plane=data_plane,
        model_repository_handlers=model_repository_handlers,
    )

    await server.add_custom_handlers(runtime)

    return server


@pytest.fixture
def rest_app(rest_server: RESTServer) -> FastAPI:
    return rest_server._app


@pytest.fixture
def rest_client(rest_app: FastAPI) -> TestClient:
    return TestClient(rest_app)
