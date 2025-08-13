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

import asyncio
from typing import Set
import pytest
import textwrap
import json

@pytest.fixture
def enable_two_workers(monkeypatch):
    """
    Force the parallel server to spawn two workers.
    """
    monkeypatch.setenv("MLSERVER_PARALLEL_WORKERS", "2")


@pytest.fixture
def pid_model_repo(tmp_path):
    """
    Creates a temporary model repo with a minimal runtime that returns its PID.
    No external files or pre-existing modules required.
    """
    mdir = tmp_path / "models" / "pid-model"
    mdir.mkdir(parents=True)

    runtime_code = textwrap.dedent("""
        import os
        from mlserver import MLModel
        from mlserver.types import InferenceRequest, InferenceResponse, ResponseOutput, Parameters
        from mlserver.codecs import StringCodec

        class PIDRuntime(MLModel):
            async def load(self) -> bool:
                return True

            async def predict(self, payload: InferenceRequest) -> InferenceResponse:
                pid_str = str(os.getpid())
                return InferenceResponse(
                    model_name=self.name,
                    outputs=[
                        ResponseOutput(
                            name="pid",
                            datatype="BYTES",
                            shape=[1],
                            data=[pid_str],
                            parameters=Parameters(content_type=StringCodec.ContentType),
                        )
                    ],
                    parameters=Parameters(headers={"x-worker-pid": pid_str}),
                )
    """)
    (mdir / "models.py").write_text(runtime_code)

    (mdir / "model-settings.json").write_text(json.dumps({
        "name": "pid-model",
        "implementation": "models.PIDRuntime"
    }))

    return tmp_path


# -------- Optional helpers used by tests below --------

def _extract_pid_from_rest_json(data) -> str:
    # Standard V2 REST shape: outputs[0].data[0] contains our PID string
    return str(data["outputs"][0]["data"][0])


def _extract_pid_from_grpc_response(resp) -> str:
    """
    Try a few shapes depending on how your gRPC stub maps the V2 response.
    We always make the runtime put the PID into outputs[0].data[0] (string),
    but depending on the generated client, it may surface as bytes.
    """
    try:
        out = resp.outputs[0]
        # Common mappings:
        if hasattr(out, "data") and out.data:
            pid = out.data[0]
        elif hasattr(out, "contents") and getattr(out.contents, "bytes_contents", None):
            pid = out.contents.bytes_contents[0]
        else:
            # Fallback: try to find any first scalar-like value
            pid = list(getattr(out, "data", []))[0]
    except Exception as e:
        raise AssertionError(f"Could not extract PID from gRPC response: {e}\nresp={resp!r}")

    if isinstance(pid, bytes):
        pid = pid.decode("utf-8", "ignore")
    return str(pid)


@pytest.mark.asyncio
async def test_parallel_workers_used_grpc(enable_two_workers, pid_model_repo, start_server, grpc_client, inference_request):
    """
    Proves that the gRPC path fans out across multiple worker processes by
    collecting distinct PIDs from responses.
    """
    async with start_server(model_repo=pid_model_repo):
        seen_pids: Set[str] = set()

        req = inference_request(model_name="pid-model", inputs=[])

        async def one_call():
            resp = await grpc_client.ModelInfer(req)
            seen_pids.add(_extract_pid_from_grpc_response(resp))

        # Warm-up calls (sequential)
        for _ in range(6):
            await one_call()

        # Concurrent fan-out to encourage distribution
        await asyncio.gather(*(one_call() for _ in range(16)))

        assert len(seen_pids) > 1, f"gRPC requests did not hit multiple workers. PIDs: {seen_pids}"





@pytest.mark.asyncio
async def test_batching_runs_on_multiple_workers(
    enable_two_workers,
    pid_model_repo,
    start_server,
    rest_client,
    make_infer_request,
    monkeypatch,
):
    """
    Verifies that batched requests are executed in worker processes and that
    across several batches, >1 worker handles traffic.
    """
    # Encourage batching without making the test slow / flaky.
    # Adjust if your suite requires different env names.
    monkeypatch.setenv("MLSERVER_MODEL_MAX_BATCH_SIZE", "8")
    monkeypatch.setenv("MLSERVER_MODEL_MAX_BATCH_TIME", "0.01")

    async with start_server(model_repo=pid_model_repo):
        seen_pids: Set[str] = set()

        async def one_call():
            body = make_infer_request(model_name="pid-model", inputs=[])
            r = await rest_client.post("/v2/models/pid-model/infer", json=body)
            r.raise_for_status()
            seen_pids.add(_extract_pid_from_rest_json(r.json()))

        # Enough concurrency to trigger multiple batches
        await asyncio.gather(*(one_call() for _ in range(24)))

        assert len(seen_pids) > 1, f"Batching did not utilize multiple workers. PIDs: {seen_pids}"




@pytest.mark.asyncio
async def test_rest_parallel_workers(enable_two_workers, pid_model_repo, start_server, rest_client, make_infer_request):
    """
    Proves the REST path is served by multiple worker processes by sampling PIDs.
    """
    async with start_server(model_repo=pid_model_repo):
        seen_pids: Set[str] = set()

        async def one_call():
            body = make_infer_request(model_name="pid-model", inputs=[])
            r = await rest_client.post("/v2/models/pid-model/infer", json=body)
            r.raise_for_status()
            seen_pids.add(_extract_pid_from_rest_json(r.json()))

        # Warm-up sequential calls then a concurrent fan-out
        for _ in range(6):
            await one_call()
        await asyncio.gather(*(one_call() for _ in range(16)))

        assert len(seen_pids) > 1, f"REST requests did not hit multiple workers. PIDs: {seen_pids}"
