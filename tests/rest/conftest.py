import pytest

from fastapi import FastAPI
from httpx import AsyncClient

from mlserver.handlers import DataPlane, ModelRepositoryHandlers
from mlserver.parallel import InferencePoolRegistry
from mlserver.batching import load_batching
from mlserver.rest import RESTServer
from mlserver.registry import MultiModelRegistry
from mlserver import Settings, ModelSettings
from prometheus_client.registry import CollectorRegistry

from ..fixtures import SumModel


@pytest.fixture
async def model_registry(
    sum_model_settings: ModelSettings, inference_pool_registry: InferencePoolRegistry
) -> MultiModelRegistry:
    model_registry = MultiModelRegistry(
        on_model_load=[inference_pool_registry.load_model, load_batching],
        on_model_reload=[inference_pool_registry.reload_model],
        on_model_unload=[inference_pool_registry.unload_model],
        model_initialiser=inference_pool_registry.model_initialiser,
    )

    model_name = sum_model_settings.name
    await model_registry.load(sum_model_settings)

    yield model_registry

    try:
        # It could be that the model is not present anymore
        await model_registry.unload(model_name)
    except Exception:
        pass


@pytest.fixture
async def rest_server(
    settings: Settings,
    data_plane: DataPlane,
    model_repository_handlers: ModelRepositoryHandlers,
    sum_model: SumModel,
    prometheus_registry: CollectorRegistry,
) -> RESTServer:
    server = RESTServer(
        settings,
        data_plane=data_plane,
        model_repository_handlers=model_repository_handlers,
    )

    sum_model = await server.add_custom_handlers(sum_model)

    yield server

    await server.delete_custom_handlers(sum_model)


@pytest.fixture
def rest_app(rest_server: RESTServer) -> FastAPI:
    return rest_server._app


@pytest.fixture
async def rest_client(rest_app: FastAPI) -> AsyncClient:
    async with AsyncClient(app=rest_app, base_url="http://test") as ac:
        yield ac
