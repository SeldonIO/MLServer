import pytest

from mlserver.errors import MLServerError
from mlserver.handlers.custom import get_custom_handlers
from mlserver.types import InferenceRequest, MetadataModelResponse
from mlserver.model import MLModel
from mlserver.settings import ModelSettings
from mlserver.parallel.pool import InferencePool
from mlserver.types import InferenceResponse
from mlserver.utils import generate_uuid
from typing import AsyncIterator, List

from ..fixtures import ErrorModel
from mlserver.parallel.model import ParallelModel, ModelMethods


@pytest.fixture
async def sum_model(inference_pool: InferencePool, sum_model: MLModel) -> MLModel:
    parallel_model = await inference_pool.load_model(sum_model)

    yield parallel_model

    await inference_pool.unload_model(sum_model)


async def test_predict(
    sum_model: MLModel,
    sum_model_settings: ModelSettings,
    inference_request: InferenceRequest,
):
    inference_response = await sum_model.predict(inference_request)

    assert inference_response.id == inference_request.id
    assert inference_response.model_name == sum_model_settings.name
    assert len(inference_response.outputs) == 1


async def test_predict_error(
    error_model: MLModel,
    inference_request: InferenceRequest,
):
    with pytest.raises(MLServerError) as excinfo:
        await error_model.predict(inference_request)

    expected_msg = f"mlserver.errors.MLServerError: {ErrorModel.error_message}"
    assert str(excinfo.value) == expected_msg


async def test_metadata(
    sum_model: MLModel,
    sum_model_settings: ModelSettings,
):
    metadata = await sum_model.metadata()

    assert isinstance(metadata, MetadataModelResponse)
    assert metadata.name == sum_model_settings.name


async def test_metadata_cached(
    sum_model: MLModel, sum_model_settings: ModelSettings, mocker
):
    expected_metadata = MetadataModelResponse(name="foo", platform="bar")

    async def _send(*args, **kwargs) -> MetadataModelResponse:
        return expected_metadata

    send_stub = mocker.stub("_send")
    send_stub.side_effect = _send
    sum_model._send = send_stub

    metadata_1 = await sum_model.metadata()
    metadata_2 = await sum_model.metadata()

    assert metadata_1 == expected_metadata
    assert metadata_2 == expected_metadata
    send_stub.assert_called_once()


async def test_custom_handlers(sum_model: MLModel):
    handlers = get_custom_handlers(sum_model)
    assert len(handlers) == 2

    response = await sum_model.my_payload([1, 2, 3])
    assert response == 6


async def test_predict_stream(
    sum_model: MLModel,
    inference_request: InferenceRequest,
    mocker,
):
    """
    Validate that ParallelModel.predict_stream forwards to the dispatcher
    streaming path and yields InferenceResponse chunks as they arrive.
    We stub the dispatcher's streaming method so no model-side streaming
    implementation is required.
    """

    # Build two fake streamed responses
    r1 = InferenceResponse(
        model_name=sum_model.settings.name, id=generate_uuid(), outputs=[]
    )
    r2 = InferenceResponse(
        model_name=sum_model.settings.name, id=generate_uuid(), outputs=[]
    )

    async def _fake_dispatch_stream(_req_msg) -> AsyncIterator[InferenceResponse]:
        # Simulate two streamed chunks from the worker
        yield r1
        yield r2

    # Patch the underlying dispatcher's streaming method
    mocker.patch.object(
        sum_model._dispatcher,  # type: ignore[attr-defined]
        "dispatch_request_stream",
        side_effect=_fake_dispatch_stream,
    )

    # Create a tiny async generator of requests (API expects an AsyncIterator)
    async def _reqs() -> AsyncIterator[InferenceRequest]:
        yield inference_request

    seen: List[InferenceResponse] = []
    async for chunk in sum_model.predict_stream(_reqs()):
        seen.append(chunk)

    assert len(seen) == 2
    assert isinstance(seen[0], InferenceResponse)
    assert isinstance(seen[1], InferenceResponse)


# ---------- Tests ----------

@pytest.mark.asyncio
async def test_predict_stream_forwards_to_dispatcher(parallel: ParallelModel, inference_request: InferenceRequest, mocker):
    """
    ParallelModel.predict_stream should forward to dispatcher.dispatch_request_stream
    with ModelMethods.PredictStream and yield incoming chunks verbatim.
    """
    r1 = InferenceResponse(model_name=parallel.settings.name, outputs=[])
    r2 = InferenceResponse(model_name=parallel.settings.name, outputs=[])

    async def _fake_stream(_req_msg) -> AsyncIterator[InferenceResponse]:
        # Validate we’re being asked for the right method name
        assert _req_msg.method_name == ModelMethods.PredictStream.value
        yield r1
        yield r2

    mocker.patch.object(
        parallel._dispatcher,  # type: ignore[attr-defined]
        "dispatch_request_stream",
        side_effect=_fake_stream,
    )

    async def _reqs() -> AsyncIterator[InferenceRequest]:
        yield inference_request

    seen: List[InferenceResponse] = []
    async for chunk in parallel.predict_stream(_reqs()):
        seen.append(chunk)

    assert seen == [r1, r2]


@pytest.mark.asyncio
async def test_parallelise_wraps_async_iterator_handlers(parallel: ParallelModel, mocker):
    """
    If an underlying model method returns AsyncIterator[...] (by annotation),
    _parallelise should create a wrapper that streams via _send_stream using that method's name.
    """
    # Grab the real inner method (for name + annotations)
    method = parallel._model.tokens  # type: ignore[attr-defined]

    # Build the wrapper the same way ParallelModel does for custom handlers
    wrapper = parallel._parallelise(method)

    # Prepare a fake streamed iterator from the dispatcher
    async def _fake_stream(_req_msg) -> AsyncIterator[int]:
        assert _req_msg.method_name == "tokens"  # must match the method.__name__
        for i in (1, 2, 3):
            yield i

    mocker.patch.object(
        parallel._dispatcher,  # type: ignore[attr-defined]
        "dispatch_request_stream",
        side_effect=_fake_stream,
    )

    # wrapper() should be an async generator; collect results
    out: List[int] = []
    async for x in wrapper():  # type: ignore[misc]
        out.append(x)

    assert out == [1, 2, 3]


@pytest.mark.asyncio
async def test_send_stream_calls_aclose(parallel: ParallelModel, mocker):
    """
    Ensure _send_stream calls aclose() on the async iterator it receives from the dispatcher.
    """
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
        return aiter  # dispatcher returns an async-iterator object

    mocker.patch.object(
        parallel._dispatcher,  # type: ignore[attr-defined]
        "dispatch_request_stream",
        side_effect=_fake_stream,
    )

    # Consume only one element to leave the iterator early and trigger the 'finally' that calls aclose()
    async def _consume_one():
        agen = parallel._send_stream("any")
        async for _ in agen:
            break
        # make sure the generator finalizes -> triggers finally -> calls aclose()
        await agen.aclose()

    await _consume_one()
    assert aiter.closed is True


@pytest.mark.asyncio
async def test_predict_returns_inference_response(parallel: ParallelModel, inference_request: InferenceRequest, mocker):
    expected = InferenceResponse(model_name=parallel.settings.name, outputs=[])

    async def _fake_dispatch(req_msg):
        # Validate method name and args
        assert req_msg.method_name == ModelMethods.Predict.value
        assert len(req_msg.method_args) == 1
        assert isinstance(req_msg.method_args[0], InferenceRequest)
        return type("Resp", (), {"return_value": expected})

    mocker.patch.object(parallel._dispatcher, "dispatch_request", side_effect=_fake_dispatch)  # type: ignore[attr-defined]

    out = await parallel.predict(inference_request)
    assert isinstance(out, InferenceResponse)
    assert out is expected


@pytest.mark.asyncio
async def test_predict_raises_on_wrong_return_type(parallel: ParallelModel, inference_request: InferenceRequest, mocker):
    async def _fake_dispatch(_):
        return type("Resp", (), {"return_value": "not-a-response"})

    mocker.patch.object(parallel._dispatcher, "dispatch_request", side_effect=_fake_dispatch)  # type: ignore[attr-defined]

    with pytest.raises(Exception):
        await parallel.predict(inference_request)


@pytest.mark.asyncio
async def test_metadata_caches_and_returns(parallel: ParallelModel, mocker):
    expected = MetadataModelResponse(name=parallel.settings.name, platform="x")

    async def _fake_dispatch(_):
        return type("Resp", (), {"return_value": expected})

    spy = mocker.patch.object(parallel._dispatcher, "dispatch_request", side_effect=_fake_dispatch)  # type: ignore[attr-defined]

    m1 = await parallel.metadata()
    m2 = await parallel.metadata()
    assert m1 is expected and m2 is expected
    spy.assert_called_once()


@pytest.mark.asyncio
async def test_metadata_raises_on_wrong_type(parallel: ParallelModel, mocker):
    async def _fake_dispatch(_):
        return type("Resp", (), {"return_value": None})

    mocker.patch.object(parallel._dispatcher, "dispatch_request", side_effect=_fake_dispatch)  # type: ignore[attr-defined]

    with pytest.raises(Exception):
        await parallel.metadata()


@pytest.mark.asyncio
async def test_predict_stream_forwards_to_dispatcher(parallel: ParallelModel, inference_request: InferenceRequest, mocker):
    r1 = InferenceResponse(model_name=parallel.settings.name, outputs=[])
    r2 = InferenceResponse(model_name=parallel.settings.name, outputs=[])

    async def _fake_stream(req_msg) -> AsyncIterator[InferenceResponse]:
        assert req_msg.method_name == ModelMethods.PredictStream.value
        # The single arg must be the payload iterator itself
        assert len(req_msg.method_args) == 1
        assert hasattr(req_msg.method_args[0], "__aiter__")
        yield r1
        yield r2

    mocker.patch.object(parallel._dispatcher, "dispatch_request_stream", side_effect=_fake_stream)  # type: ignore[attr-defined]

    async def _reqs():
        yield inference_request

    out: List[InferenceResponse] = []
    async for c in parallel.predict_stream(_reqs()):
        out.append(c)
    assert out == [r1, r2]


@pytest.mark.asyncio
async def test_send_stream_calls_aclose_on_early_exit(parallel: ParallelModel, mocker):
    class AIter:
        def __init__(self):
            self._i = 0
            self.closed = False
        def __aiter__(self): return self
        async def __anext__(self):
            if self._i >= 2:
                raise StopAsyncIteration
            self._i += 1
            return self._i
        async def aclose(self):
            self.closed = True

    aiter = AIter()

    async def _fake_stream(_req_msg):
        return aiter  # return an async-iterator object (not a generator function)

    mocker.patch.object(parallel._dispatcher, "dispatch_request_stream", side_effect=_fake_stream)  # type: ignore[attr-defined]

    agen = parallel._send_stream("any")
    async for _ in agen:
        break
    # Explicitly close the outer generator so its `finally` runs and calls aclose() on inner iterator.
    await agen.aclose()
    assert aiter.closed is True


@pytest.mark.asyncio
async def test_send_stream_bubbles_exception_and_closes(parallel: ParallelModel, mocker):
    class BoomIter:
        def __init__(self):
            self.closed = False
            self.emitted = False
        def __aiter__(self): return self
        async def __anext__(self):
            if not self.emitted:
                self.emitted = True
                return 1
            raise RuntimeError("boom")
        async def aclose(self):
            self.closed = True

    aiter = BoomIter()

    async def _fake_stream(_req_msg):
        return aiter

    mocker.patch.object(parallel._dispatcher, "dispatch_request_stream", side_effect=_fake_stream)  # type: ignore[attr-defined]

    agen = parallel._send_stream("m")
    with pytest.raises(RuntimeError):
        async for _ in agen:
            pass
    # Even on error, the finally should run and close the inner iterator.
    assert aiter.closed is True


@pytest.mark.asyncio
async def test_send_stream_accepts_coroutine_returning_iterator(parallel: ParallelModel, mocker):
    async def _aiter():
        for i in (10, 20):
            yield i

    async def _fake_stream(_req_msg):
        # Return a coroutine that produces an async-generator (iterator)
        async def _coro():
            return _aiter()
        return await _coro()

    mocker.patch.object(parallel._dispatcher, "dispatch_request_stream", side_effect=_fake_stream)  # type: ignore[attr-defined]

    got = []
    async for x in parallel._send_stream("foo"):
        got.append(x)
    assert got == [10, 20]


@pytest.mark.asyncio
async def test_parallelise_wraps_custom_async_iterator(parallel: ParallelModel, mocker):
    method = parallel._model.tokens  # type: ignore[attr-defined]
    wrapper = parallel._parallelise(method)

    async def _fake_stream(_req_msg) -> AsyncIterator[int]:
        assert _req_msg.method_name == "tokens"
        for i in (1, 2, 3):
            yield i

    mocker.patch.object(parallel._dispatcher, "dispatch_request_stream", side_effect=_fake_stream)  # type: ignore[attr-defined]

    out = []
    async for x in wrapper():  # type: ignore[misc]
        out.append(x)
    assert out == [1, 2, 3]


@pytest.mark.asyncio
async def test_parallelise_wraps_builtin_predict_stream_and_passes_iterator(parallel: ParallelModel, mocker):
    method = parallel._model.predict_stream  # type: ignore[attr-defined]
    wrapper = parallel._parallelise(method)

    seen_iter = {"same_obj": False}

    async def _fake_stream(_req_msg) -> AsyncIterator[InferenceResponse]:
        # Must use the original method name, not the enum
        assert _req_msg.method_name == "predict_stream"
        assert len(_req_msg.method_args) == 1
        # Ensure the passed iterator is exactly the same object
        assert id(_req_msg.method_args[0]) == id(payloads)
        # Produce two chunks
        yield InferenceResponse(model_name=parallel.settings.name, outputs=[])
        yield InferenceResponse(model_name=parallel.settings.name, outputs=[])

    mocker.patch.object(parallel._dispatcher, "dispatch_request_stream", side_effect=_fake_stream)  # type: ignore[attr-defined]

    async def _payloads():
        yield InferenceRequest(inputs=[])

    payloads = _payloads()

    got = []
    async for r in wrapper(payloads):  # type: ignore[misc]
        got.append(r)
    assert len(got) == 2 and all(isinstance(r, InferenceResponse) for r in got)


@pytest.mark.asyncio
async def test_predict_stream_passes_iterator_by_reference(parallel: ParallelModel, inference_request: InferenceRequest, mocker):
    async def _reqs():
        yield inference_request

    it = _reqs()

    async def _fake_stream(req_msg) -> AsyncIterator[InferenceResponse]:
        # The iterator we receive should be the exact same object
        assert id(req_msg.method_args[0]) == id(it)
        # Return a tiny generator
        async def _gen():
            yield InferenceResponse(model_name=parallel.settings.name, outputs=[])
        return _gen()

    mocker.patch.object(parallel._dispatcher, "dispatch_request_stream", side_effect=_fake_stream)  # type: ignore[attr-defined]

    got = []
    async for ch in parallel.predict_stream(it):
        got.append(ch)
    assert len(got) == 1
