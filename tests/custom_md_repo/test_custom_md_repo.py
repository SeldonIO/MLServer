import asyncio
import os
from time import sleep
from uuid import UUID
import json
import pytest

from mlserver.settings import ModelSettings, Settings
from tempfile import TemporaryDirectory
from prometheus_client.registry import REGISTRY, CollectorRegistry
from starlette_exporter import PrometheusMiddleware

from mlserver.server import MLServer
from mlserver.settings import Settings, ModelSettings
from tests.custom_md_repo.conftest import rest_client
from tests.custom_md_repo.dummymdrepo import DummyModelRepository

from ..utils import RESTClient


async def get_ml_server(
    settings: Settings,
    prometheus_registry: CollectorRegistry,  # noqa: F811
    model_repository: DummyModelRepository,
):
    server = MLServer(settings)
    server_task = asyncio.create_task(server.start())
    model_settings_list = await model_repository.list()
    await server._model_registry.load(model_settings_list[0])

    yield server

    await server.stop()
    await server_task


async def test_custom_model_repo_by_param(
    settings: Settings, prometheus_registry: CollectorRegistry
):
    model_repository = DummyModelRepository(
        {"files": ["tests/custom_md_repo/testdata/model-settings.json"]}
    )

    aserver = get_ml_server(settings, prometheus_registry, model_repository)
    server = await aserver.asend(None)

    try:
        http_server = f"{settings.host}:{settings.http_port}"
        client = RESTClient(http_server)

        await client.wait_until_model_ready("sum-model")

        result = await client.list_models()

        assert len(result) == 1
    except Exception as ex:
        print(ex)
        raise ex


async def test_custom_model_repo_by_settings(
    rest_client: RESTClient,
    settings: Settings,
):

    await rest_client.wait_until_model_ready("sum-model")

    result = await rest_client.list_models()

    assert len(result) == 1
