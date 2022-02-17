import pytest

from pytest_cases import parametrize_with_cases, fixture
from mlserver import Settings
from aiohttp.client_exceptions import ClientResponseError

from .utils import MetricsClient


@fixture
@parametrize_with_cases("metrics_endpoint")
def settings(settings: Settings, metrics_endpoint: str) -> Settings:
    settings.metrics_endpoint = metrics_endpoint
    return settings


async def test_metrics(metrics_client: MetricsClient):
    await metrics_client.wait_until_ready()

    if metrics_client._metrics_endpoint is None:
        # Assert metrics are disabled
        metrics_client._metrics_endpoint = "/metrics"
        with pytest.raises(ClientResponseError) as err:
            await metrics_client.metrics()
        assert err.value.status == 404
    else:
        # Otherwise, assert all metrics are present
        metrics = await metrics_client.metrics()
        assert metrics is not None

        expected_prefixes = ("python_", "process_", "rest_server_", "grpc_server_")
        metrics_list = list(iter(metrics))
        assert len(metrics_list) > 0
        for metric in metrics_list:
            assert metric.name.startswith(expected_prefixes)
