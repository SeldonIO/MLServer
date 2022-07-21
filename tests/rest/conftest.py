import pytest

from fastapi import FastAPI
from httpx import AsyncClient

from mlserver.handlers import DataPlane, ModelRepositoryHandlers
from mlserver.parallel import InferencePool
from mlserver.batching import load_batching
from mlserver.rest import RESTServer
from mlserver import Settings

from ..fixtures import SumModel


@pytest.fixture
async def rest_server(
    settings: Settings,
    data_plane: DataPlane,
    model_repository_handlers: ModelRepositoryHandlers,
    inference_pool: InferencePool,
    sum_model: SumModel,
) -> RESTServer:
    server = RESTServer(
        settings,
        data_plane=data_plane,
        model_repository_handlers=model_repository_handlers,
    )

    sum_model = await inference_pool.load_model(sum_model)
    sum_model = await server.add_custom_handlers(sum_model)
    sum_model = await load_batching(sum_model)

    yield server

    sum_model = await inference_pool.unload_model(sum_model)
    sum_model = await server.delete_custom_handlers(sum_model)


@pytest.fixture
def rest_app(rest_server: RESTServer) -> FastAPI:
    return rest_server._app


@pytest.fixture
async def rest_client(rest_app: FastAPI) -> AsyncClient:
    async with AsyncClient(app=rest_app, base_url="http://test") as ac:
        yield ac
