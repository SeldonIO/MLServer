"""The `llmman serve` client, and `oci://` model URIs.

The daemon protocol is exercised against a real HTTP server on a loopback port
rather than mocks, so the NDJSON streaming contract is genuinely tested.
"""

import http.server
import json
import socketserver
import tempfile
import threading
from unittest.mock import patch

import pytest

from mlserver import llmman
from mlserver.model import MLModel
from mlserver.settings import ModelParameters, ModelSettings
from mlserver.utils import get_model_uri


def _ndjson(*objs):
    return "".join(json.dumps(o) + "\n" for o in objs)


class _FakeDaemon:
    """A minimal stand-in for `llmman serve`, on a real loopback port."""

    def __init__(self):
        self.version = {"version": "0.1.0", "pid": 1}
        self.pull_body = _ndjson({"status": "success"})
        self.pull_status = 200
        self.last_request = None
        daemon = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def _send(self, status, body, ctype):
                raw = body.encode()
                self.send_response(status)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)

            def do_GET(self):
                self._send(200, json.dumps(daemon.version), "application/json")

            def do_POST(self):
                length = int(self.headers.get("Content-Length", 0))
                daemon.last_request = json.loads(self.rfile.read(length))
                self._send(daemon.pull_status, daemon.pull_body, "application/x-ndjson")

        self._server = socketserver.TCPServer(("127.0.0.1", 0), Handler)
        self.url = f"http://127.0.0.1:{self._server.server_address[1]}"
        threading.Thread(target=self._server.serve_forever, daemon=True).start()

    def close(self):
        self._server.shutdown()
        self._server.server_close()


@pytest.fixture
def daemon():
    d = _FakeDaemon()
    yield d
    d.close()


def test_accepts_a_llmman_daemon(daemon):
    llmman.check_daemon(daemon.url)


def test_rejects_a_non_llmman_server(daemon):
    daemon.version = {"hello": "world"}
    with pytest.raises(RuntimeError, match="not an llmman daemon"):
        llmman.check_daemon(daemon.url)


def test_reports_nothing_listening_actionably():
    with pytest.raises(RuntimeError, match="llmman serve"):
        llmman.check_daemon("http://127.0.0.1:1")


def test_pull_succeeds_and_forwards_progress(daemon):
    daemon.pull_body = _ndjson(
        {"status": "pulling manifest"},
        {"status": "pulling blobs", "completed": 50, "total": 100},
        {"status": "success"},
    )
    seen = []
    llmman.pull(daemon.url, "ghcr.io/org/model:tag", lambda *a: seen.append(a))

    assert daemon.last_request == {"model": "ghcr.io/org/model:tag"}
    assert seen == [("pulling manifest", 0, 0), ("pulling blobs", 50, 100)]


def test_reports_an_in_band_error_at_http_200(daemon):
    # The daemon streams errors in-band, so a 200 does not mean success.
    daemon.pull_body = _ndjson({"status": "pulling"}, {"error": "unauthorized"})
    with pytest.raises(RuntimeError, match="unauthorized"):
        llmman.pull(daemon.url, "ref")


def test_rejects_a_stream_that_ends_without_success(daemon):
    daemon.pull_body = _ndjson({"status": "pulling blobs"})
    with pytest.raises(RuntimeError, match="without reporting success"):
        llmman.pull(daemon.url, "ref")


def test_reports_a_non_ok_status(daemon):
    daemon.pull_status = 400
    daemon.pull_body = '{"error":"bad request"}'
    with pytest.raises(RuntimeError):
        llmman.pull(daemon.url, "ref")


def test_tolerates_a_non_json_diagnostic_line(daemon):
    daemon.pull_body = "not json\n" + _ndjson({"status": "success"})
    llmman.pull(daemon.url, "ref")


def test_recognizes_the_oci_scheme():
    assert llmman.is_oci_uri("oci://ghcr.io/org/model:tag")
    assert llmman.is_oci_uri("OCI://ghcr.io/org/model:tag")


@pytest.mark.parametrize(
    "value",
    [
        "s3://bucket/key",
        "gs://bucket/key",
        "file:///models/my-model.bin",
        "my-model.bin",
        "/an/absolute/path/my-model.bin",
        "",
        None,
    ],
)
def test_leaves_every_other_uri_alone(value):
    # rclone-style remotes and plain paths must never be claimed.
    assert not llmman.is_oci_uri(value)


@pytest.mark.parametrize(
    "bad",
    [
        "",
        "   \n\n",
        "not json",
        '["a", "list"]',
        '{"no_path": 1}',
        '{"path": ""}',
        '{"path": "/nonexistent/xyzzy"}',
    ],
)
def test_rejects_malformed_resolve_output(bad):
    with pytest.raises(RuntimeError):
        llmman.parse_resolve_output(bad, "ref")


def test_parses_the_resolve_contract():
    with tempfile.TemporaryDirectory() as path:
        line = json.dumps({"reference": "r", "path": path, "format": "safetensors"})
        assert llmman.parse_resolve_output(line, "r") == path
        # A leaked diagnostic must not break resolution.
        assert llmman.parse_resolve_output(f"pulling...\n{line}\n", "r") == path


@pytest.mark.parametrize(
    "host,want",
    [
        ("", "http://127.0.0.1:17434"),
        ("1.2.3.4:9999", "http://1.2.3.4:9999"),
        ("1.2.3.4", "http://1.2.3.4:17434"),
        # A wildcard bind is meaningful to the server but not to a client.
        ("0.0.0.0:9999", "http://127.0.0.1:9999"),
        ("[::]:9999", "http://[::1]:9999"),
    ],
)
def test_endpoint_parsing(monkeypatch, host, want):
    monkeypatch.setenv(llmman.HOST_ENV, host)
    assert llmman.endpoint() == want


async def test_get_model_uri_resolves_an_oci_uri():
    """An oci:// uri is pulled, then treated as an ordinary local path."""
    model_settings = ModelSettings(
        implementation=MLModel,
        parameters=ModelParameters(uri="oci://ghcr.io/org/model:tag"),
    )
    with (
        patch("mlserver.llmman.resolve_uri", return_value="/resolved/model") as resolve,
        patch("os.path.isfile", return_value=True),
    ):
        model_uri = await get_model_uri(model_settings)

    assert model_uri == "/resolved/model"
    resolve.assert_called_once_with("oci://ghcr.io/org/model:tag")


async def test_get_model_uri_leaves_an_s3_uri_alone():
    model_settings = ModelSettings(
        implementation=MLModel, parameters=ModelParameters(uri="s3://bucket/key")
    )
    with patch("mlserver.llmman.resolve_uri") as resolve:
        model_uri = await get_model_uri(model_settings)

    resolve.assert_not_called()
    assert model_uri == "s3://bucket/key"
