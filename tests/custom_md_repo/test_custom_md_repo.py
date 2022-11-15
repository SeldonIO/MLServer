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

from ..utils import RESTClient


async def test_custom_model_repo_by_settings(
    rest_client: RESTClient,
    settings: Settings,
):

    await rest_client.wait_until_model_ready("sum-model")

    result = await rest_client.list_models()

    assert len(result) > 0
