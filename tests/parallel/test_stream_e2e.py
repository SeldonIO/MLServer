# tests/parallel/test_stream_e2e.py
import asyncio
import pytest
from typing import AsyncIterator, List

from mlserver.model import MLModel
from mlserver.settings import ModelSettings
from mlserver.types import InferenceRequest, InferenceResponse, MetadataModelResponse
from mlserver.codecs.string import StringCodec
from mlserver.parallel.model import ParallelModel


# -------- Model that streams one character per chunk --------


class ParallelCharStreamModel(ParallelModel):
    async def predict_stream(
        self, payloads: AsyncIterator[InferenceRequest]
    ) -> AsyncIterator[InferenceResponse]:
        # read only the first request
        req = None
        async for r in payloads:
            req = r
            break
        if req is None or not req.inputs:
            return

        decoded = StringCodec.decode_input(req.inputs[0])
        if not decoded:
            return

        for ch in decoded:
            # tiny delay to simulate streaming
            await asyncio.sleep(0.001)
            yield InferenceResponse(
                model_name=self.settings.name,
                outputs=[
                    # make sure we return a ResponseOutput (not a plain list)
                    StringCodec.encode_output(
                        name="output",
                        payload=[ch],
                        use_bytes=True,  # IMPORTANT
                    )
                ],
            )


# ------------------ Fixtures ------------------


@pytest.fixture
def model_settings() -> ModelSettings:
    return ModelSettings(
        name="char-stream-model",
        implementation=ParallelCharStreamModel,
        parallel_workers=2,
        parameters={"version": "v-test"},
    )


@pytest.fixture
def char_stream_model(
    model_settings: ModelSettings, dispatcher
) -> ParallelCharStreamModel:
    # Minimal inner model to satisfy ParallelModel's constructor
    class _Inner(MLModel):
        async def load(self):
            return

        async def predict(self, _):
            return InferenceResponse(model_name=self.settings.name, outputs=[])

        async def metadata(self):
            return MetadataModelResponse(name=self.settings.name, platform="dummy")

    inner = _Inner(model_settings)
    return ParallelCharStreamModel(inner, dispatcher)


@pytest.fixture
def req_text() -> InferenceRequest:
    return InferenceRequest(
        inputs=[
            # IMPORTANT: use_bytes=True so decode_input returns a single string
            StringCodec.encode_input(
                name="input", payload="hello streaming world", use_bytes=True
            )
        ]
    )


@pytest.fixture
def req_empty() -> InferenceRequest:
    return InferenceRequest(
        inputs=[StringCodec.encode_input(name="input", payload="", use_bytes=True)]
    )


@pytest.fixture
def req_punct() -> InferenceRequest:
    return InferenceRequest(
        inputs=[
            StringCodec.encode_input(name="input", payload="hi, world!", use_bytes=True)
        ]
    )


# ------------------ Tests ------------------


@pytest.mark.asyncio
async def test_stream_chars_happy_path(
    char_stream_model: ParallelCharStreamModel, req_text: InferenceRequest
):
    async def _reqs():
        yield req_text

    pieces: List[str] = []
    async for chunk in char_stream_model.predict_stream(_reqs()):
        pieces.append(StringCodec.decode_output(chunk.outputs[0])[0])

    assert pieces == list("hello streaming world")
    assert "".join(pieces) == "hello streaming world"


@pytest.mark.asyncio
async def test_stream_empty_input_yields_no_chunks(
    char_stream_model: ParallelCharStreamModel, req_empty: InferenceRequest
):
    async def _reqs():
        yield req_empty

    pieces = [
        StringCodec.decode_output(c.outputs[0])[0]
        async for c in char_stream_model.predict_stream(_reqs())
    ]
    assert pieces == []  # nothing to stream


@pytest.mark.asyncio
async def test_stream_punctuation_as_chars(
    char_stream_model: ParallelCharStreamModel, req_punct: InferenceRequest
):
    async def _reqs():
        yield req_punct

    pieces = [
        StringCodec.decode_output(c.outputs[0])[0]
        async for c in char_stream_model.predict_stream(_reqs())
    ]
    assert pieces == list("hi, world!")
    assert "".join(pieces) == "hi, world!"


@pytest.mark.asyncio
async def test_stream_early_exit_and_close(
    char_stream_model: ParallelCharStreamModel, req_text: InferenceRequest
):
    async def _reqs():
        yield req_text

    agen = char_stream_model.predict_stream(_reqs())

    # read just the first char then close
    first = None
    async for chunk in agen:
        first = StringCodec.decode_output(chunk.outputs[0])[0]
        break

    assert first == "h"
    await agen.aclose()


@pytest.fixture
def req_no_inputs() -> InferenceRequest:
    # A request that has *no* inputs at all
    return InferenceRequest(inputs=[])


@pytest.fixture
def req_unicode() -> InferenceRequest:
    # Simple Unicode including an emoji that’s a single code point
    s = "héllö 😊🚀"
    return InferenceRequest(
        inputs=[StringCodec.encode_input(name="input", payload=s, use_bytes=True)]
    )


@pytest.fixture
def req_long() -> InferenceRequest:
    # Keep it reasonably short so the test stays fast (~0.12s given 0.001s per char)
    s = "abcde" * 24  # 120 chars
    return InferenceRequest(
        inputs=[StringCodec.encode_input(name="input", payload=s, use_bytes=True)]
    )


@pytest.mark.asyncio
async def test_stream_no_payloads_yields_no_chunks(
    char_stream_model: ParallelCharStreamModel,
):
    async def _no_reqs():
        if False:
            yield  # never yield anything

    pieces = [
        StringCodec.decode_output(c.outputs[0])[0]
        async for c in char_stream_model.predict_stream(_no_reqs())
    ]
    assert pieces == []


@pytest.mark.asyncio
async def test_stream_request_with_no_inputs_yields_no_chunks(
    char_stream_model: ParallelCharStreamModel,
    req_no_inputs: InferenceRequest,
):
    async def _reqs():
        yield req_no_inputs

    pieces = [
        StringCodec.decode_output(c.outputs[0])[0]
        async for c in char_stream_model.predict_stream(_reqs())
    ]
    assert pieces == []


@pytest.mark.asyncio
async def test_only_first_request_is_consumed(
    char_stream_model: ParallelCharStreamModel,
    req_text: InferenceRequest,
    req_punct: InferenceRequest,
):
    class TrackingReqs:
        def __init__(self, first, second):
            self.calls = 0
            self._first = first
            self._second = second

        def __aiter__(self):
            return self

        async def __anext__(self):
            # The model should consume exactly one item, then never ask again.
            if self.calls == 0:
                self.calls += 1
                return self._first
            if self.calls == 1:
                self.calls += 1
                return self._second
            raise StopAsyncIteration

    tracker = TrackingReqs(req_text, req_punct)

    # Consume the entire char stream from the *first* request
    out = [
        StringCodec.decode_output(c.outputs[0])[0]
        async for c in char_stream_model.predict_stream(tracker)
    ]
    assert "".join(out) == "hello streaming world"
    # Should have pulled only the first request from the iterator
    assert tracker.calls == 1


@pytest.mark.asyncio
async def test_concurrent_streams(char_stream_model: ParallelCharStreamModel):
    async def _make_reqs(s: str):
        yield InferenceRequest(
            inputs=[StringCodec.encode_input(name="input", payload=s, use_bytes=True)]
        )

    async def _collect(s: str):
        return [
            StringCodec.decode_output(c.outputs[0])[0]
            async for c in char_stream_model.predict_stream(_make_reqs(s))
        ]

    s1 = "abc 123"
    s2 = "xyz!"
    p1, p2 = await asyncio.gather(_collect(s1), _collect(s2))
    assert "".join(p1) == s1
    assert "".join(p2) == s2


@pytest.mark.asyncio
async def test_stream_unicode_chars(
    char_stream_model: ParallelCharStreamModel, req_unicode: InferenceRequest
):
    async def _reqs():
        yield req_unicode

    pieces = [
        StringCodec.decode_output(c.outputs[0])[0]
        async for c in char_stream_model.predict_stream(_reqs())
    ]
    assert "".join(pieces) == "héllö 😊🚀"
    assert pieces == list("héllö 😊🚀")


@pytest.mark.asyncio
async def test_stream_large_input(
    char_stream_model: ParallelCharStreamModel, req_long: InferenceRequest
):
    async def _reqs():
        yield req_long

    pieces = [
        StringCodec.decode_output(c.outputs[0])[0]
        async for c in char_stream_model.predict_stream(_reqs())
    ]
    joined = "".join(pieces)
    assert len(pieces) == len(joined)  # one char per chunk
    assert joined.startswith("abcde")
    assert joined.endswith("abcde")


@pytest.mark.asyncio
async def test_each_chunk_has_single_output_value(
    char_stream_model: ParallelCharStreamModel, req_punct: InferenceRequest
):
    async def _reqs():
        yield req_punct

    async for chunk in char_stream_model.predict_stream(_reqs()):
        # One ResponseOutput per chunk
        assert len(chunk.outputs) == 1
        # StringCodec.decode_output returns a list of strings
        decoded = StringCodec.decode_output(chunk.outputs[0])
        assert isinstance(decoded, list)
        assert len(decoded) == 1
        assert isinstance(decoded[0], str)
        break  # one sample is enough for structure checks
