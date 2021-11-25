from .conftest import MetricsClient


async def test_metrics(metrics_client: MetricsClient):
    await metrics_client.wait_until_ready()
    metrics = await metrics_client.metrics()

    assert metrics is not None

    expected_prefixes = ("python_", "process_", "starlette_")
    metrics_list = list(iter(metrics))
    assert len(metrics_list) > 0
    for metric in metrics_list:
        assert metric.name.startswith(expected_prefixes)
