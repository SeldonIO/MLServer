import pytest
from pytest_cases import parametrize, fixture_ref

from typing import AsyncGenerator

from grpc import StatusCode
from mlserver import Settings, ModelSettings
from mlserver.grpc.interceptors import PromServerInterceptor
from mlserver.codecs import StringCodec
from mlserver.grpc import converters
from mlserver.grpc.server import GRPCServer
from mlserver.grpc.dataplane_pb2_grpc import GRPCInferenceServiceStub
from mlserver.grpc import dataplane_pb2 as pb

from ..conftest import (
    text_model,
    text_model_settings,
    text_stream_model,
    settings_stream,
    text_stream_model_settings,
)
from ..fixtures import SumModel


@parametrize("sum_model", [fixture_ref(text_model)])
@parametrize("sum_model_settings", [fixture_ref(text_model_settings)])
async def test_prometheus_unary_unary(
    grpc_server: GRPCServer,
    inference_service_stub: AsyncGenerator[GRPCInferenceServiceStub, None],
    model_generate_request: pb.ModelInferRequest,
    sum_model: SumModel,
    sum_model_settings: ModelSettings,
):
    # send 10 requests
    num_requests = 10
    for _ in range(num_requests):
        _ = await inference_service_stub.ModelInfer(model_generate_request)

    grpc_type = "UNARY"
    grpc_service_name = "inference.GRPCInferenceService"
    grpc_method_name = "ModelInfer"
    prom_interceptor = [
        interceptor
        for interceptor in grpc_server._interceptors
        if isinstance(interceptor, PromServerInterceptor)
    ][0]

    # get the number of requests intercepted
    counted_requests = (
        prom_interceptor._interceptor._metrics["grpc_server_started_counter"]
        .labels(
            grpc_type,
            grpc_service_name,
            grpc_method_name,
        )
        ._value.get()
    )

    # get the number of ok responses intercepted
    counted_responses = (
        prom_interceptor._interceptor._grpc_server_handled_total_counter.labels(
            grpc_type,
            grpc_service_name,
            grpc_method_name,
            StatusCode.OK.name,
        )._value.get()
    )

    assert int(counted_requests) == num_requests
    assert int(counted_requests) == int(counted_responses)


@parametrize("settings", [fixture_ref(settings_stream)])
@parametrize("sum_model", [fixture_ref(text_stream_model)])
@pytest.mark.parametrize("model_name", ["text-stream-model"])
@parametrize("sum_model_settings", [fixture_ref(text_stream_model_settings)])
async def test_prometheus_stream_stream(
    grpc_server: GRPCServer,
    inference_service_stub: AsyncGenerator[GRPCInferenceServiceStub, None],
    model_generate_request: pb.ModelInferRequest,
    model_name: str,
    settings: Settings,
    sum_model: SumModel,
    sum_model_settings: ModelSettings,
):
    model_generate_request.model_name = model_name

    async def get_stream_request(request):
        yield request

    # send 10 requests
    num_requests = 10
    for _ in range(num_requests):
        _ = [
            _
            async for _ in inference_service_stub.ModelStreamInfer(
                get_stream_request(model_generate_request)
            )
        ]

    grpc_type = "BIDI_STREAMING"
    grpc_service_name = "inference.GRPCInferenceService"
    grpc_method_name = "ModelStreamInfer"
    prom_interceptor = [
        interceptor
        for interceptor in grpc_server._interceptors
        if isinstance(interceptor, PromServerInterceptor)
    ][0]

    # get the number of requests intercepted
    counted_requests = (
        prom_interceptor._interceptor._metrics["grpc_server_stream_msg_received"]
        .labels(
            grpc_type,
            grpc_service_name,
            grpc_method_name,
        )
        ._value.get()
    )

    # get the number of ok responses intercepted
    counted_responses = (
        prom_interceptor._interceptor._metrics["grpc_server_stream_msg_sent"]
        .labels(
            grpc_type,
            grpc_service_name,
            grpc_method_name,
        )
        ._value.get()
    )

    inference_request_g = converters.ModelInferRequestConverter.to_types(
        model_generate_request
    )

    # we count the number of words because
    # each word is gonna be streamed back
    request_text = StringCodec.decode_input(inference_request_g.inputs[0])[0]
    num_words = len(request_text.split())

    assert int(counted_requests) >= num_requests
    assert int(counted_requests) * num_words == int(counted_responses)
