import pytest

from fastapi import FastAPI
from httpx import AsyncClient

from mlserver.handlers import DataPlane, ModelRepositoryHandlers
from mlserver.parallel import InferencePool
from mlserver.batching import load_batching
from mlserver.rest import RESTServer
from mlserver.registry import MultiModelRegistry
from mlserver import Settings, ModelSettings
from prometheus_client.registry import REGISTRY, CollectorRegistry
from starlette_exporter import PrometheusMiddleware

from ..fixtures import SumModel

@pytest.fixture()
def delete_registry() -> CollectorRegistry:
    """
    Fixture used to ensure the registry is cleaned on each run.
    Otherwise, `py-grpc-prometheus` will complain that metrics already exist.

    TODO: Open issue in `py-grpc-prometheus` to check whether a metric exists
    before creating it.
    For an example on how to do this, see `starlette_exporter`'s implementation

        https://github.com/stephenhillier/starlette_exporter/blob/947d4d631dd9a6a8c1071b45573c5562acba4834/starlette_exporter/middleware.py#L67
    """
    # NOTE: Since the `REGISTRY` object is global, this fixture is NOT
    # thread-safe!!
    collectors = list(REGISTRY._collector_to_names.keys())
    for collector in collectors:
        REGISTRY.unregister(collector)

    # Clean metrics from `starlette_exporter` as well, as otherwise they won't
    # get re-created
    PrometheusMiddleware._metrics.clear()

    yield REGISTRY

@pytest.fixture
async def model_registry(
    sum_model_settings: ModelSettings, inference_pool: InferencePool
) -> MultiModelRegistry:
    model_registry = MultiModelRegistry(
        on_model_load=[inference_pool.load_model, load_batching],
        on_model_reload=[inference_pool.reload_model],
        on_model_unload=[inference_pool.unload_model],
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
