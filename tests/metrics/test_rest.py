import asyncio

from mlserver.model import MLModel
from mlserver.types import InferenceRequest

from ..utils import RESTClient
from .utils import MetricsClient, find_metric


async def test_rest_metrics(
    metrics_client: MetricsClient,
    rest_client: RESTClient,
    inference_request: InferenceRequest,
    sum_model: MLModel,
):
    await rest_client.wait_until_ready()
    metric_name = "rest_server_requests"

    # Get metrics for REST server before sending any requests
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
