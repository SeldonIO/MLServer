import pytest
import asyncio
import os

from aiofiles.os import path

from mlserver import metrics
from mlserver.server import MLServer
from mlserver.model import MLModel
from mlserver.settings import ModelSettings
from mlserver.types import InferenceRequest, InferenceResponse
from mlserver.metrics.context import SELDON_MODEL_NAME_LABEL

from ..utils import RESTClient
from .utils import MetricsClient, find_metric

CUSTOM_METRIC_NAME = "my_custom_metric"


class CustomMetricsModel(MLModel):
    async def load(self) -> bool:
        metrics.register(CUSTOM_METRIC_NAME, "Test custom counter")
        self.reqs = 0
        return True

    async def predict(self, req: InferenceRequest) -> InferenceResponse:
        self.reqs += 1
        metrics.log(my_custom_metric=self.reqs)
        return InferenceResponse(model_name=self.name, outputs=[])


@pytest.fixture
async def custom_metrics_model(mlserver: MLServer) -> MLModel:
    model_settings = ModelSettings(
        name="custom-metrics-model", implementation=CustomMetricsModel
    )
    return await mlserver._model_registry.load(model_settings)


async def test_db_files(
    custom_metrics_model: MLModel,
    rest_client: RESTClient,
    mlserver: MLServer,
    inference_request: InferenceRequest,
):
    # Ensure each worker gets a request / response so that it can create the
    # relevant metric files
    await rest_client.wait_until_ready()
    await asyncio.gather(
        *[
            rest_client.infer(custom_metrics_model.name, inference_request)
            for _ in range(mlserver._settings.parallel_workers)
        ]
    )

    assert mlserver._settings.parallel_workers > 0
    default_pool = mlserver._inference_pool_registry._default_pool
    for pid in default_pool._workers:
        db_file = os.path.join(mlserver._settings.metrics_dir, f"histogram_{pid}.db")
        assert await path.isfile(db_file)


async def test_custom_metrics(
    custom_metrics_model: MLModel,
    inference_request: InferenceRequest,
    metrics_client: MetricsClient,
    rest_client: RESTClient,
):
    await rest_client.wait_until_ready()

    metrics = await metrics_client.metrics()
    custom_counter = find_metric(metrics, CUSTOM_METRIC_NAME)
    assert custom_counter is None

    expected_value = 5
    await asyncio.gather(
        *[
            rest_client.infer(custom_metrics_model.name, inference_request)
            for _ in range(expected_value)
        ]
    )

    metrics = await metrics_client.metrics()
    custom_metric = find_metric(metrics, CUSTOM_METRIC_NAME)
    assert custom_metric is not None

    last_bucket = custom_metric.samples[-1]
    assert last_bucket.value == expected_value
    assert SELDON_MODEL_NAME_LABEL in last_bucket.labels
    assert last_bucket.labels[SELDON_MODEL_NAME_LABEL] == custom_metrics_model.name
