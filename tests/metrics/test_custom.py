import pytest
import asyncio
import os

from aiofiles.os import path
from prometheus_client import Counter

from mlserver.server import MLServer
from mlserver.model import MLModel
from mlserver.settings import ModelSettings
from mlserver.types import InferenceRequest, InferenceResponse

from ..utils import RESTClient
from .utils import MetricsClient, find_metric

COUNTER_NAME = "my_custom_counter"


class CustomMetricsModel(MLModel):
    async def load(self) -> bool:
        self.counter = Counter(COUNTER_NAME, "Test custom counter")
        self.ready = True
        return self.ready

    async def predict(self, req: InferenceRequest) -> InferenceResponse:
        self.counter.inc()
        return InferenceResponse(model_name=self.name, outputs=[])


@pytest.fixture
async def custom_metrics_model(mlserver: MLServer) -> MLModel:
    model_settings = ModelSettings(
        name="custom-metrics-model", implementation=CustomMetricsModel
    )
    return await mlserver._model_registry.load(model_settings)


async def test_db_files(
    custom_metrics_model: MLModel, rest_client: RESTClient, mlserver: MLServer
):
    await rest_client.wait_until_ready()

    assert mlserver._settings.parallel_workers > 0
    for pid in mlserver._inference_pool._workers:
        db_file = os.path.join(mlserver._settings.metrics_dir, f"counter_{pid}.db")
        assert await path.isfile(db_file)


async def test_custom_metrics(
    custom_metrics_model: MLModel,
    inference_request: InferenceRequest,
    metrics_client: MetricsClient,
    rest_client: RESTClient,
):
    await rest_client.wait_until_ready()

    metrics = await metrics_client.metrics()
    custom_counter = find_metric(metrics, COUNTER_NAME)
    assert custom_counter is not None
    assert len(custom_counter.samples) == 1
    assert custom_counter.samples[0].value == 0

    expected_value = 5
    await asyncio.gather(
        *[
            rest_client.infer(custom_metrics_model.name, inference_request)
            for _ in range(expected_value)
        ]
    )

    metrics = await metrics_client.metrics()
    custom_counter = find_metric(metrics, COUNTER_NAME)
    assert custom_counter is not None
    assert len(custom_counter.samples) == 1
    assert custom_counter.samples[0].value == expected_value
