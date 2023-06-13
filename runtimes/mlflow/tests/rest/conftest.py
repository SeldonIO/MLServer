import pytest

from fastapi import FastAPI
from httpx import AsyncClient
from typing import Iterable, AsyncIterable
from prometheus_client.registry import REGISTRY, CollectorRegistry
from starlette_exporter import PrometheusMiddleware

from mlserver.handlers import DataPlane, ModelRepositoryHandlers
from mlserver.registry import MultiModelRegistry
from mlserver.rest import RESTServer
from mlserver.repository import ModelRepository, SchemalessModelRepository
from mlserver.model import MLModel
from mlserver.metrics.registry import MetricsRegistry, REGISTRY as METRICS_REGISTRY
from mlserver.parallel import InferencePoolRegistry
from mlserver import Settings, ModelSettings

from .utils import unregister_metrics


@pytest.fixture
def metrics_registry() -> Iterable[MetricsRegistry]:
    yield METRICS_REGISTRY

    unregister_metrics(METRICS_REGISTRY)


@pytest.fixture
def prometheus_registry(
    metrics_registry: MetricsRegistry,
) -> Iterable[CollectorRegistry]:
    """
    Fixture used to ensure the registry is cleaned on each run.
    Otherwise, `py-grpc-prometheus` will complain that metrics already exist.

    TODO: Open issue in `py-grpc-prometheus` to check whether a metric exists
    before creating it.
    For an example on how to do this, see `starlette_exporter`'s implementation

        https://github.com/stephenhillier/starlette_exporter/blob/947d4d631dd9a6a8c1071b45573c5562acba4834/starlette_exporter/middleware.py#L67
    """
    yield REGISTRY

    unregister_metrics(REGISTRY)

    # Clean metrics from `starlette_exporter` as well, as otherwise they won't
    # get re-created
    PrometheusMiddleware._metrics.clear()


@pytest.fixture
async def inference_pool_registry(
    settings: Settings,
) -> AsyncIterable[InferencePoolRegistry]:
    registry = InferencePoolRegistry(settings)
    yield registry

    await registry.close()


@pytest.fixture
def model_repository(model_uri: str) -> ModelRepository:
    return SchemalessModelRepository(model_uri)


@pytest.fixture
async def model_registry(
    inference_pool_registry: InferencePoolRegistry, model_settings: ModelSettings
) -> AsyncIterable[MultiModelRegistry]:
    model_registry = MultiModelRegistry(
        on_model_load=[inference_pool_registry.load_model],
        on_model_reload=[inference_pool_registry.reload_model],
        on_model_unload=[inference_pool_registry.unload_model],
        model_initialiser=inference_pool_registry.model_initialiser,
    )

    await model_registry.load(model_settings)

    yield model_registry

    await model_registry.unload(model_settings.name)


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
    runtime: MLModel,
    prometheus_registry: CollectorRegistry,
) -> AsyncIterable[RESTServer]:
    server = RESTServer(
        settings,
        data_plane=data_plane,
        model_repository_handlers=model_repository_handlers,
    )

    await server.add_custom_handlers(runtime)

    yield server

    await server.delete_custom_handlers(runtime)


@pytest.fixture
def rest_app(rest_server: RESTServer) -> FastAPI:
    return rest_server._app


@pytest.fixture
async def rest_client(rest_app: FastAPI) -> AsyncIterable[AsyncClient]:
    async with AsyncClient(app=rest_app, base_url="http://test") as ac:
        yield ac
