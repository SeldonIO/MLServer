import grpc
import pytest
from pytest_lazyfixture import lazy_fixture


from mlserver.cloudevents import (
    CLOUDEVENTS_HEADER_SPECVERSION_DEFAULT,
    CLOUDEVENTS_HEADER_SPECVERSION,
)
from mlserver.grpc import dataplane_pb2 as pb
from mlserver.grpc.converters import (
    InferTensorContentsConverter,
    InferInputTensorConverter,
    InferOutputTensorConverter,
)
from mlserver.raw import pack, unpack
from mlserver.types import Datatype
from mlserver import __version__


async def test_server_live(inference_service_stub):
    req = pb.ServerLiveRequest()
    response = await inference_service_stub.ServerLive(req)

    assert response.live


async def test_server_ready(inference_service_stub):
    req = pb.ServerReadyRequest()
    response = await inference_service_stub.ServerReady(req)

    assert response.ready


async def test_model_ready(inference_service_stub, sum_model):
    req = pb.ModelReadyRequest(name=sum_model.name, version=sum_model.version)
    response = await inference_service_stub.ModelReady(req)

    assert response.ready


async def test_server_metadata(inference_service_stub):
    req = pb.ServerMetadataRequest()
    response = await inference_service_stub.ServerMetadata(req)

    assert response.name == "mlserver"
    assert response.version == __version__
    assert response.extensions == []


async def test_model_metadata(inference_service_stub, sum_model_settings):
    req = pb.ModelMetadataRequest(
        name=sum_model_settings.name, version=sum_model_settings.parameters.version
    )
    response = await inference_service_stub.ModelMetadata(req)

    assert response.name == sum_model_settings.name
    assert response.platform == sum_model_settings.platform
    assert response.versions == sum_model_settings.versions


@pytest.mark.parametrize(
    "model_name,model_version", [("sum-model", "v1.2.3"), ("sum-model", None)]
)
async def test_model_infer(
    inference_service_stub,
    model_infer_request,
    model_name,
    model_version,
):
    model_infer_request.model_name = model_name
    if model_version is not None:
        model_infer_request.model_version = model_version
    else:
        model_infer_request.ClearField("model_version")

    prediction = await inference_service_stub.ModelInfer(model_infer_request)
    expected = pb.InferTensorContents(int64_contents=[6])

    assert len(prediction.outputs) == 1
    assert prediction.outputs[0].contents == expected


@pytest.mark.parametrize("settings", [lazy_fixture("settings_stream")])
@pytest.mark.parametrize(
    "sum_model_settings", [lazy_fixture("text_stream_model_settings")]
)
@pytest.mark.parametrize("sum_model", [lazy_fixture("text_stream_model")])
@pytest.mark.parametrize(
    "model_name,model_version",
    [("text-stream-model", "v1.2.3"), ("text-stream-model", None)],
)
async def test_model_stream_infer(
    inference_service_stub,
    model_generate_request,
    model_name,
    model_version,
):
    model_generate_request.model_name = model_name
    if model_version is not None:
        model_generate_request.model_version = model_version
    else:
        model_generate_request.ClearField("model_version")

    i = -1
    text = ["What", " is", " the", " capital", " of", " France?"]

    async def get_stream_request(request):
        yield request

    async for prediction in inference_service_stub.ModelStreamInfer(
        get_stream_request(model_generate_request)
    ):
        i += 1
        expected = pb.InferTensorContents(bytes_contents=[text[i].encode()])
        assert len(prediction.outputs) == 1
        assert prediction.outputs[0].contents == expected


async def test_model_infer_raw_contents(inference_service_stub, model_infer_request):
    # Prepare request with raw contents
    for input_tensor in model_infer_request.inputs:
        request_input = InferInputTensorConverter.to_types(input_tensor)
        packed = pack(request_input)
        model_infer_request.raw_input_contents.append(packed)
        input_tensor.ClearField("contents")

    prediction = await inference_service_stub.ModelInfer(model_infer_request)

    # Convert raw output into contents field
    for output_tensor, raw_output in zip(
        prediction.outputs, prediction.raw_output_contents
    ):
        response_output = InferOutputTensorConverter.to_types(output_tensor)
        data = unpack(response_output, raw_output)
        contents = InferTensorContentsConverter.from_types(
            data, Datatype(response_output.datatype)
        )
        output_tensor.contents.CopyFrom(contents)

    expected = pb.InferTensorContents(int64_contents=[6])

    assert len(prediction.outputs) == 1
    assert prediction.outputs[0].contents == expected


async def test_model_infer_headers(
    inference_service_stub,
    model_infer_request,
    sum_model_settings,
):
    model_infer_request.model_name = sum_model_settings.name
    model_infer_request.ClearField("model_version")

    request_metadata = (("x-foo", "bar"),)
    inference_call = inference_service_stub.ModelInfer(
        model_infer_request, metadata=request_metadata
    )

    expected_ce_headers = (
        (
            CLOUDEVENTS_HEADER_SPECVERSION.lower(),
            CLOUDEVENTS_HEADER_SPECVERSION_DEFAULT,
        ),
    )
    trailing_metadata = await inference_call.trailing_metadata()
    for key, value in request_metadata + expected_ce_headers:
        assert key in trailing_metadata
        assert trailing_metadata[key] == value


async def test_model_infer_error(inference_service_stub, model_infer_request):
    with pytest.raises(grpc.RpcError) as err:
        model_infer_request.model_name = "my-model"
        await inference_service_stub.ModelInfer(model_infer_request)

    assert err.value.code() == grpc.StatusCode.NOT_FOUND
    assert err.value.details() == "Model my-model with version v1.2.3 not found"


@pytest.mark.parametrize("settings", [lazy_fixture("settings_stream")])
@pytest.mark.parametrize(
    "sum_model_settings", [lazy_fixture("text_stream_model_settings")]
)
@pytest.mark.parametrize("sum_model", [lazy_fixture("text_stream_model")])
async def test_model_stream_infer_error(inference_service_stub, model_generate_request):
    async def get_stream_request(request):
        yield request

    with pytest.raises(grpc.RpcError) as err:
        model_generate_request.model_name = "my-model"
        async for _ in inference_service_stub.ModelStreamInfer(
            get_stream_request(model_generate_request)
        ):
            pass

    assert err.value.code() == grpc.StatusCode.NOT_FOUND
    assert err.value.details() == "Model my-model with version v1.2.3 not found"


async def test_model_repository_index(
    inference_service_stub,
    grpc_repository_index_request,
):
    index = await inference_service_stub.RepositoryIndex(grpc_repository_index_request)

    assert len(index.models) == 1


async def test_model_repository_unload(inference_service_stub, sum_model_settings):
    unload_request = pb.RepositoryModelUnloadRequest(model_name=sum_model_settings.name)
    await inference_service_stub.RepositoryModelUnload(unload_request)

    with pytest.raises(grpc.RpcError):
        await inference_service_stub.ModelMetadata(
            pb.ModelMetadataRequest(name=sum_model_settings.name)
        )


async def test_model_repository_load(
    inference_service_stub,
    sum_model_settings,
):
    await inference_service_stub.RepositoryModelUnload(
        pb.RepositoryModelLoadRequest(model_name=sum_model_settings.name)
    )
    load_request = pb.RepositoryModelLoadRequest(model_name=sum_model_settings.name)
    await inference_service_stub.RepositoryModelLoad(load_request)

    response = await inference_service_stub.ModelMetadata(
        pb.ModelMetadataRequest(name=sum_model_settings.name)
    )

    assert response.name == sum_model_settings.name


async def test_model_repository_load_error(inference_service_stub, sum_model_settings):
    with pytest.raises(grpc.RpcError) as err:
        load_request = pb.RepositoryModelLoadRequest(model_name="my-model")
        await inference_service_stub.RepositoryModelLoad(load_request)

    assert err.value.code() == grpc.StatusCode.NOT_FOUND
    assert err.value.details() == "Model my-model not found"


async def test_infer_invalid_datatype_error(
    inference_service_stub,
    model_infer_request_invalid_datatype,
):
    model_infer_request_invalid_datatype.model_name = "sum-model"
    model_infer_request_invalid_datatype.ClearField("model_version")

    with pytest.raises(grpc.aio.AioRpcError) as exc_info:
        _ = await inference_service_stub.ModelInfer(
            model_infer_request_invalid_datatype
        )

    assert exc_info.value.details() == (
        "1 validation error for RequestInput\ndatatype\n  Input should be "
        "'BOOL', 'UINT8', 'UINT16', 'UINT32', 'UINT64', 'INT8', 'INT16', "
        "'INT32', 'INT64', 'FP16', 'FP32', 'FP64' or 'BYTES' [type=enum, "
        "input_value='INT322', input_type=str]\n    For further "
        "information visit https://errors.pydantic.dev/2.9/v/enum"
    )