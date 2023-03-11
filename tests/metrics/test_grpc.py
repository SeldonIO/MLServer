import pytest
import asyncio

from typing import AsyncGenerator

from grpc import aio

from mlserver.grpc import dataplane_pb2 as pb
from mlserver.grpc.dataplane_pb2_grpc import GRPCInferenceServiceStub
from mlserver.server import MLServer
from mlserver.settings import Settings

from .utils import MetricsClient, find_metric

# Import fixture from `grpc` module
from ..grpc.conftest import model_infer_request  # noqa: F401


@pytest.fixture
async def inference_service_stub(
    mlserver: MLServer, settings: Settings
) -> AsyncGenerator[GRPCInferenceServiceStub, None]:
    async with aio.insecure_channel(f"{settings.host}:{settings.grpc_port}") as channel:
        yield GRPCInferenceServiceStub(channel)


async def test_grpc_metrics(
    metrics_client: MetricsClient,
    inference_service_stub: GRPCInferenceServiceStub,
    model_infer_request: pb.ModelInferRequest,  # noqa: F811
):
    await metrics_client.wait_until_ready()
    metric_name = "grpc_server_handled"

    # Get metrics for gRPC server before sending any requests
    metrics = await metrics_client.metrics()
    grpc_server_handled = find_metric(metrics, metric_name)
    assert grpc_server_handled is None

    expected_handled = 5
    await asyncio.gather(
        *[
            inference_service_stub.ModelInfer(model_infer_request)
            for _ in range(expected_handled)
        ]
    )

    # Get metrics for gRPC server after sending a few requests
    metrics = await metrics_client.metrics()
    grpc_server_handled = find_metric(metrics, metric_name)
    assert grpc_server_handled is not None
    assert len(grpc_server_handled.samples) == 1
    assert grpc_server_handled.samples[0].value == expected_handled
