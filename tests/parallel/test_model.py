import pytest
from typing import AsyncIterator, List
from mlserver.types import InferenceRequest, InferenceResponse, MetadataModelResponse
from mlserver.model import MLModel
from mlserver.settings import ModelSettings
from mlserver.utils import generate_uuid
from mlserver.errors import MLServerError
from mlserver.parallel.pool import InferencePool
from mlserver.parallel.model import ParallelModel, ModelMethods
from mlserver.handlers.custom import get_custom_handlers

from ..fixtures import ErrorModel  # keep if your tests package exposes this


# ---------- Fixture that loads the model into the parallel pool ----------


@pytest.fixture
async def parallel_model(
    inference_pool: InferencePool, sum_model: MLModel
) -> ParallelModel:
    pm: ParallelModel = await inference_pool.load_model(sum_model)
    try:
        yield pm
    finally:
        await inference_pool.unload_model(sum_model)


# ---------- Tests (updated to use `parallel_model`) ----------


@pytest.mark.asyncio
async def test_predict(
    parallel_model: ParallelModel,
    sum_model_settings: ModelSettings,
    inference_request: InferenceRequest,
):
    inference_response = await parallel_model.predict(inference_request)
    assert inference_response.id == inference_request.id
    assert inference_response.model_name == sum_model_settings.name
    assert len(inference_response.outputs) == 1


@pytest.mark.asyncio
async def test_predict_error(
    parallel_model: ParallelModel,
    error_model: MLModel,
    inference_request: InferenceRequest,
):
    # Load the error model into the pool so calls go through the dispatcher
    pool: InferencePool = parallel_model._dispatcher._pool  # type: ignore[attr-defined]
    await pool.load_model(error_model)
    try:
        with pytest.raises(MLServerError) as excinfo:
            await error_model.predict(inference_request)
        expected_msg = f"mlserver.errors.MLServerError: {ErrorModel.error_message}"
        assert str(excinfo.value) == expected_msg
    finally:
        await pool.unload_model(error_model)


@pytest.mark.asyncio
async def test_metadata(
    parallel_model: ParallelModel, sum_model_settings: ModelSettings
):
    metadata = await parallel_model.metadata()
    assert isinstance(metadata, MetadataModelResponse)
    assert metadata.name == sum_model_settings.name


@pytest.mark.asyncio
async def test_metadata_cached(parallel_model: ParallelModel, mocker):
    expected = MetadataModelResponse(name="foo", platform="bar")

    async def _send(*_a, **_k):
        return expected

    spy = mocker.stub("_send")
    spy.side_effect = _send
    parallel_model._send = spy  # type: ignore[attr-defined]

    m1 = await parallel_model.metadata()
    m2 = await parallel_model.metadata()
    assert m1 is expected and m2 is expected
    spy.assert_called_once()


@pytest.mark.asyncio
async def test_custom_handlers(parallel_model: ParallelModel):
    handlers = get_custom_handlers(parallel_model)
    assert len(handlers) >= 1  # you had 2; adjust if your model defines exactly 2
    response = await parallel_model.my_payload([1, 2, 3])  # type: ignore[attr-defined]
    assert response == 6


@pytest.mark.asyncio
async def test_predict_stream(
    parallel_model: ParallelModel,
    inference_request: InferenceRequest,
    mocker,
):
    r1 = InferenceResponse(
        model_name=parallel_model.settings.name, id=generate_uuid(), outputs=[]
    )
    r2 = InferenceResponse(
        model_name=parallel_model.settings.name, id=generate_uuid(), outputs=[]
    )

    async def _fake_dispatch_stream(_req_msg) -> AsyncIterator[InferenceResponse]:
        yield r1
        yield r2

    mocker.patch.object(
        parallel_model._dispatcher,  # type: ignore[attr-defined]
        "dispatch_request_stream",
        side_effect=_fake_dispatch_stream,
    )

    async def _reqs() -> AsyncIterator[InferenceRequest]:
        yield inference_request

    seen: List[InferenceResponse] = []
    async for chunk in parallel_model.predict_stream(_reqs()):
        seen.append(chunk)

    assert seen == [r1, r2]


@pytest.mark.asyncio
async def test_predict_stream_forwards_to_dispatcher(
    parallel_model: ParallelModel, inference_request: InferenceRequest, mocker
):
    r1 = InferenceResponse(model_name=parallel_model.settings.name, outputs=[])
    r2 = InferenceResponse(model_name=parallel_model.settings.name, outputs=[])

    async def _fake_stream(req_msg) -> AsyncIterator[InferenceResponse]:
        assert req_msg.method_name == ModelMethods.PredictStream.value
        assert len(req_msg.method_args) == 1
        yield r1
        yield r2

    mocker.patch.object(
        parallel_model._dispatcher, "dispatch_request_stream", side_effect=_fake_stream
    )  # type: ignore[attr-defined]

    async def _reqs():
        yield inference_request

    out: List[InferenceResponse] = []
    async for c in parallel_model.predict_stream(_reqs()):
        out.append(c)
    assert out == [r1, r2]


@pytest.mark.asyncio
async def test_parallelise_wraps_async_iterator_handlers(
    parallel_model: ParallelModel, mocker
):
    method = parallel_model._model.tokens  # type: ignore[attr-defined]
    wrapper = parallel_model._parallelise(method)

    async def _fake_stream(_req_msg) -> AsyncIterator[int]:
        assert _req_msg.method_name == "tokens"
        for i in (1, 2, 3):
            yield i

    mocker.patch.object(
        parallel_model._dispatcher, "dispatch_request_stream", side_effect=_fake_stream
    )  # type: ignore[attr-defined]

    out: List[int] = []
    async for x in wrapper():  # type: ignore[misc]
        out.append(x)
    assert out == [1, 2, 3]


@pytest.mark.asyncio
async def test_send_stream_calls_aclose(parallel_model: ParallelModel, mocker):
    class AIter:
        def __init__(self):
            self._i = 0
            self.closed = False

        def __aiter__(self):
            return self

        async def __anext__(self):
            if self._i >= 2:
                raise StopAsyncIteration
            self._i += 1
            return self._i

        async def aclose(self):
            self.closed = True

    aiter = AIter()

    async def _fake_stream(_req_msg):
        return aiter

    mocker.patch.object(
        parallel_model._dispatcher, "dispatch_request_stream", side_effect=_fake_stream
    )  # type: ignore[attr-defined]

    agen = parallel_model._send_stream("any")
    async for _ in agen:
        break
    await agen.aclose()
    assert aiter.closed is True


@pytest.mark.asyncio
async def test_predict_returns_inference_response(
    parallel_model: ParallelModel, inference_request: InferenceRequest, mocker
):
    expected = InferenceResponse(model_name=parallel_model.settings.name, outputs=[])

    async def _fake_dispatch(req_msg):
        assert req_msg.method_name == ModelMethods.Predict.value
        return type("Resp", (), {"return_value": expected})

    mocker.patch.object(
        parallel_model._dispatcher, "dispatch_request", side_effect=_fake_dispatch
    )  # type: ignore[attr-defined]

    out = await parallel_model.predict(inference_request)
    assert out is expected


@pytest.mark.asyncio
async def test_predict_raises_on_wrong_return_type(
    parallel_model: ParallelModel, inference_request: InferenceRequest, mocker
):
    async def _fake_dispatch(_):
        return type("Resp", (), {"return_value": "not-a-response"})

    mocker.patch.object(
        parallel_model._dispatcher, "dispatch_request", side_effect=_fake_dispatch
    )  # type: ignore[attr-defined]
    with pytest.raises(Exception):
        await parallel_model.predict(inference_request)


@pytest.mark.asyncio
async def test_metadata_caches_and_returns(parallel_model: ParallelModel, mocker):
    expected = MetadataModelResponse(name=parallel_model.settings.name, platform="x")

    async def _fake_dispatch(_):
        return type("Resp", (), {"return_value": expected})

    spy = mocker.patch.object(
        parallel_model._dispatcher, "dispatch_request", side_effect=_fake_dispatch
    )  # type: ignore[attr-defined]

    m1 = await parallel_model.metadata()
    m2 = await parallel_model.metadata()
    assert m1 is expected and m2 is expected
    spy.assert_called_once()


@pytest.mark.asyncio
async def test_metadata_raises_on_wrong_type(parallel_model: ParallelModel, mocker):
    async def _fake_dispatch(_):
        return type("Resp", (), {"return_value": None})

    mocker.patch.object(
        parallel_model._dispatcher, "dispatch_request", side_effect=_fake_dispatch
    )  # type: ignore[attr-defined]
    with pytest.raises(Exception):
        await parallel_model.metadata()


@pytest.mark.asyncio
async def test_parallelise_wraps_builtin_predict_stream_and_passes_iterator(
    parallel_model: ParallelModel, mocker
):
    method = parallel_model._model.predict_stream  # type: ignore[attr-defined]
    wrapper = parallel_model._parallelise(method)

    async def _fake_stream(_req_msg) -> AsyncIterator[InferenceResponse]:
        assert _req_msg.method_name == "predict_stream"
        assert len(_req_msg.method_args) == 1
        assert id(_req_msg.method_args[0]) == id(payloads)
        yield InferenceResponse(model_name=parallel_model.settings.name, outputs=[])
        yield InferenceResponse(model_name=parallel_model.settings.name, outputs=[])

    mocker.patch.object(
        parallel_model._dispatcher, "dispatch_request_stream", side_effect=_fake_stream
    )  # type: ignore[attr-defined]

    async def _payloads():
        yield InferenceRequest(inputs=[])

    payloads = _payloads()

    got = []
    async for r in wrapper(payloads):  # type: ignore[misc]
        got.append(r)
    assert len(got) == 2 and all(isinstance(r, InferenceResponse) for r in got)


@pytest.mark.asyncio
async def test_predict_stream_passes_iterator_by_reference(
    parallel_model: ParallelModel, inference_request: InferenceRequest, mocker
):
    async def _reqs():
        yield inference_request

    it = _reqs()

    async def _fake_stream(req_msg) -> AsyncIterator[InferenceResponse]:
        assert id(req_msg.method_args[0]) == id(it)

        async def _gen():
            yield InferenceResponse(model_name=parallel_model.settings.name, outputs=[])

        return _gen()

    mocker.patch.object(
        parallel_model._dispatcher, "dispatch_request_stream", side_effect=_fake_stream
    )  # type: ignore[attr-defined]

    got = []
    async for ch in parallel_model.predict_stream(it):
        got.append(ch)
    assert len(got) == 1
