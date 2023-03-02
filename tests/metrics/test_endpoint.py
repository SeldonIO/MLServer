import pytest

from pytest_cases import parametrize_with_cases, fixture
from aiohttp.client_exceptions import ClientConnectorError

from mlserver import Settings, MLModel
from mlserver.types import InferenceRequest

from ..utils import RESTClient
from .utils import MetricsClient


@fixture
@parametrize_with_cases("metrics_endpoint")
def settings(settings: Settings, metrics_endpoint: str) -> Settings:
    settings.metrics_endpoint = metrics_endpoint
    return settings


async def test_metrics(
    rest_client: RESTClient,
    metrics_client: MetricsClient,
    inference_request: InferenceRequest,
    sum_model: MLModel,
):
    await rest_client.wait_until_ready()
    await rest_client.infer(sum_model.name, inference_request)

    if metrics_client._metrics_endpoint is None:
        # Assert metrics are disabled
        metrics_client._metrics_endpoint = "/metrics"
        with pytest.raises(ClientConnectorError):
            await metrics_client.metrics()
    else:
        # Otherwise, assert all metrics are present
        metrics = await metrics_client.metrics()
        assert metrics is not None

        expected_prefixes = (
            "python_",
            "process_",
            "rest_server_",
            "grpc_server_",
            "model_infer_",
            "batch_request_",
            "parallel_request_",
        )
        metrics_list = list(iter(metrics))
        assert len(metrics_list) > 0
        for metric in metrics_list:
            assert metric.name.startswith(expected_prefixes)
