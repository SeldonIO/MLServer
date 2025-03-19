import pytest
import asyncio

from mlserver.model import MLModel
from mlserver.types import InferenceRequest
from mlserver.server import MLServer
from mlserver.settings import Settings
from mlserver.metrics.context import SELDON_MODEL_NAME_LABEL

from ..utils import RESTClient
from .utils import MetricsClient, find_metric


@pytest.fixture
async def rest_client(mlserver: MLServer, settings: Settings):
    http_server = f"{settings.host}:{settings.http_port}"
    return RESTClient(http_server)


async def test_parallel_queue_metrics(
    metrics_client: MetricsClient,
    rest_client: RESTClient,
    inference_request: InferenceRequest,
    sum_model: MLModel,
):
    await rest_client.wait_until_ready()
    metric_name = "parallel_request_queue"

    expected_handled = 5
    await asyncio.gather(
        *[
            rest_client.infer(sum_model.name, inference_request)
            for _ in range(expected_handled)
        ]
    )

    metrics = await metrics_client.metrics()
    parallel_request_queue = find_metric(metrics, metric_name)
    assert parallel_request_queue is not None
    assert len(parallel_request_queue.samples) != 0


async def test_batch_queue_metrics(
    metrics_client: MetricsClient,
    rest_client: RESTClient,
    inference_request: InferenceRequest,
    sum_model: MLModel,
):
    await rest_client.wait_until_ready()
    metric_name = "batch_request_queue"

    expected_handled = 5
    await asyncio.gather(
        *[
            rest_client.infer(sum_model.name, inference_request)
            for _ in range(expected_handled)
        ]
    )

    import time

    time.sleep(10)

    metrics = await metrics_client.metrics()
    batch_request_queue = find_metric(metrics, metric_name)
    assert batch_request_queue is not None
    assert len(batch_request_queue.samples) != 0

    last_bucket = batch_request_queue.samples[-1]
    assert SELDON_MODEL_NAME_LABEL in last_bucket.labels
    assert last_bucket.labels[SELDON_MODEL_NAME_LABEL] == sum_model.name
