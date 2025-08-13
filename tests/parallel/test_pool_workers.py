import os
import asyncio
import pytest
from typing import AsyncIterator, List, Set, Optional

from mlserver.model import MLModel
from mlserver.settings import ModelSettings
from mlserver.types import InferenceRequest, InferenceResponse, MetadataModelResponse
from mlserver.codecs.string import StringCodec
from mlserver.parallel.pool import InferencePool

# ---------------- Worker-side PID models ----------------


class PidUnaryModel(MLModel):
    async def load(self) -> None:
        return

    async def metadata(self) -> MetadataModelResponse:
        return MetadataModelResponse(name=self.settings.name, platform="test")

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        # Return this worker's PID as the single string output
        return InferenceResponse(
            model_name=self.settings.name,
            outputs=[
                StringCodec.encode_output(
                    name="output", payload=[str(os.getpid())], use_bytes=False
                )
            ],
        )


class PidStreamModel(MLModel):
    async def load(self) -> None:  # fast load
        return

    async def predict_stream(
        self, payloads: Optional[AsyncIterator[InferenceRequest]] = None
    ) -> AsyncIterator[InferenceResponse]:
        """
        Ignore payloads entirely so we don't need to ship an async iterator
        across processes. Stream exactly one chunk containing the worker PID.
        """
        pid = str(os.getpid())
        # tiny delay to look like a real stream
        await asyncio.sleep(0.001)
        yield InferenceResponse(
            model_name=self.settings.name,
            outputs=[StringCodec.encode_output("output", [pid], use_bytes=True)],
        )


# ---------------- Settings helpers ----------------


@pytest.fixture
def pid_unary_settings() -> ModelSettings:
    return ModelSettings(
        name="pid-unary",
        implementation=PidUnaryModel,
        parallel_workers=2,  # <-- what we're asserting about
        parameters={"version": "v-test"},
    )


@pytest.fixture
def pid_stream_settings() -> ModelSettings:
    return ModelSettings(
        name="pid-stream",
        implementation=PidStreamModel,
        parallel_workers=2,  # <-- what we're asserting about
        parameters={"version": "v-test"},
    )


# ---------------- Requests ----------------


@pytest.fixture
def trivial_req() -> InferenceRequest:
    # Only needed to keep the fixture shape similar to others
    return InferenceRequest(
        inputs=[StringCodec.encode_input("input", payload="x", use_bytes=True)]
    )


# ---------------- Tests ----------------


@pytest.mark.asyncio
async def test_pool_uses_two_workers_unary(
    inference_pool: InferencePool,
    pid_unary_settings: ModelSettings,
    trivial_req: InferenceRequest,
):
    """
    Load a unary model with parallel_workers=2, fire many requests concurrently,
    and assert we see at least two distinct worker PIDs in the responses.
    """
    model = PidUnaryModel(pid_unary_settings)
    parallel_model = await inference_pool.load_model(model)

    # (Optional) sanity: dispatcher really has 2 workers
    disp = getattr(parallel_model, "_dispatcher", None)
    if disp is not None and hasattr(disp, "_workers"):
        assert len(disp._workers) == 2  # type: ignore[attr-defined]

    async def call_once():
        out = await parallel_model.predict(trivial_req)
        return StringCodec.decode_output(out.outputs[0])[0]

    # Send a small burst; round-robin should hit both workers
    pids: Set[str] = set(await asyncio.gather(*(call_once() for _ in range(8))))
    assert len(pids) >= 2, f"Expected requests to hit 2 workers, saw PIDs: {pids}"

    await inference_pool.unload_model(model)


@pytest.mark.asyncio
async def test_pool_uses_two_workers_streaming(
    inference_pool: InferencePool,
    pid_stream_settings: ModelSettings,
    trivial_req: InferenceRequest,
):
    model = PidStreamModel(pid_stream_settings)
    parallel_model = await inference_pool.load_model(model)

    # Sanity: pool has two workers
    disp = getattr(parallel_model, "_dispatcher", None)
    if disp is not None and hasattr(disp, "_workers"):
        assert len(disp._workers) == 2  # type: ignore[attr-defined]

    async def run_one_stream() -> str:
        # IMPORTANT: pass a picklable sentinel instead of an async generator
        agen = parallel_model.predict_stream(None)  # <- avoids pickling error
        pieces: List[str] = []
        try:

            async def _consume():
                async for c in agen:
                    pieces.append(StringCodec.decode_output(c.outputs[0])[0])

            await asyncio.wait_for(_consume(), timeout=3.0)
        finally:
            await agen.aclose()

        assert len(pieces) == 1
        return pieces[0]  # PID

    seen_pids: Set[str] = set()
    for _ in range(6):
        pid = await run_one_stream()
        seen_pids.add(pid)

    assert (
        len(seen_pids) >= 2
    ), f"Expected streams to hit 2 workers, got PIDs: {seen_pids}"

    await inference_pool.unload_model(model)
