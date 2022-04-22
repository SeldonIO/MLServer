import pytest

from fastapi import FastAPI
from httpx import AsyncClient
from typing import AsyncIterable

from mlserver.handlers import DataPlane, ModelRepositoryHandlers
from mlserver.registry import MultiModelRegistry
from mlserver.rest import RESTServer
from mlserver.repository import ModelRepository
from mlserver.model import MLModel
from mlserver import Settings, ModelSettings

from mlserver_mlflow import MLflowRuntime


@pytest.fixture
def model_repository(model_uri: str) -> ModelRepository:
    return ModelRepository(model_uri)


@pytest.fixture
async def model_registry(model_settings: ModelSettings) -> MultiModelRegistry:
    model_registry = MultiModelRegistry()
    await model_registry.load(model_settings)
    return model_registry


@pytest.fixture
async def runtime(
    model_registry: MultiModelRegistry, model_settings: ModelSettings
) -> MLModel:
    return await model_registry.get_model(model_settings.name)


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
async def rest_client(rest_app: FastAPI) -> AsyncIterable[AsyncClient]:
    async with AsyncClient(app=rest_app, base_url="http://test") as ac:
        yield ac
