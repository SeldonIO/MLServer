import pytest
import asyncio

from mlserver.model import MLModel
from mlserver.types import InferenceRequest
from mlserver.server import MLServer
from mlserver.settings import Settings

from ..utils import RESTClient
from .utils import MetricsClient, find_metric


@pytest.fixture
async def rest_client(mlserver: MLServer, settings: Settings):
    http_server = f"{settings.host}:{settings.http_port}"
    return RESTClient(http_server)


async def test_rest_metrics(
    metrics_client: MetricsClient,
    rest_client: RESTClient,
    inference_request: InferenceRequest,
    sum_model: MLModel,
):
    await rest_client.wait_until_ready()
    metric_name = "rest_server_requests"

    # Get metrics for gRPC server before sending any requests
    metrics = await metrics_client.metrics()
    rest_server_requests = find_metric(metrics, metric_name)
    assert rest_server_requests is None

    expected_handled = 5
    await asyncio.gather(
        *[
            rest_client.infer(sum_model.name, inference_request)
            for _ in range(expected_handled)
        ]
    )

    metrics = await metrics_client.metrics()
    rest_server_requests = find_metric(metrics, metric_name)
    assert rest_server_requests is not None
    assert len(rest_server_requests.samples) == 1
    assert rest_server_requests.samples[0].value == expected_handled

async def test_rest_queue_metrics(
    metrics_client: MetricsClient,
    rest_client: RESTClient,
    inference_request: InferenceRequest,
    sum_model: MLModel,
):
    await rest_client.wait_until_ready()
    metric_name = "worker_queue_request"

    expected_handled = 5
    await asyncio.gather(
        *[
            rest_client.infer(sum_model.name, inference_request)
            for _ in range(expected_handled)
        ]
    )

    metrics = await metrics_client.metrics()
    worker_queue_request = find_metric(metrics, metric_name)
    assert worker_queue_request is not None
    assert len(worker_queue_request.samples) != 0

async def test_rest_batch_metrics(
    metrics_client: MetricsClient,
    rest_client: RESTClient,
    inference_request: InferenceRequest,
    sum_model: MLModel,
):
    await rest_client.wait_until_ready()
    metric_name = "batch_queue_request_counter"

    expected_handled = 5
    await asyncio.gather(
        *[
            rest_client.infer(sum_model.name, inference_request)
            for _ in range(expected_handled)
        ]
    )

    metrics = await metrics_client.metrics()
    batch_queue_request_counter = find_metric(metrics, metric_name)
    assert batch_queue_request_counter is not None
    assert len(batch_queue_request_counter.samples) != 0

   