import asyncio
import os
import signal
from typing import Dict, Optional
from unittest.mock import patch

import pytest

from mlserver.model import MLModel
from mlserver.settings import ModelSettings, ModelParameters
from mlserver.types import InferenceRequest, InferenceResponse, Parameters
from mlserver.utils import (
    get_model_uri,
    extract_headers,
    insert_headers,
    AsyncManager,
    EventLoopBackend,
)

test_get_model_uri_paramaters = [
    ("s3://bucket/key", None, "s3://bucket/key"),
    ("s3://bucket/key", "/mnt/models/model-settings.json", "s3://bucket/key"),
]
for scheme in ["", "file:"]:
    for uri, source, expected in [
        ("my-model.bin", None, "my-model.bin"),
        (
            "my-model.bin",
            "./my-model-folder/model-settings.json",
            "my-model-folder/my-model.bin",
        ),
        (
            "my-model.bin",
            "./my-model-folder/../model-settings.json",
            "my-model.bin",
        ),
        (
            "/an/absolute/path/my-model.bin",
            "/mnt/models/model-settings.json",
            "/an/absolute/path/my-model.bin",
        ),
    ]:
        test_get_model_uri_paramaters.append((scheme + uri, source, expected))


@pytest.mark.parametrize(
    "uri, source, expected",
    test_get_model_uri_paramaters,
)
async def test_get_model_uri(uri: str, source: Optional[str], expected: str):
    model_settings = ModelSettings(
        implementation=MLModel, parameters=ModelParameters(uri=uri)
    )
    model_settings._source = source
    with patch("os.path.isfile", return_value=True):
        model_uri = await get_model_uri(model_settings)

    assert model_uri == expected


@pytest.mark.parametrize(
    "parameters",
    [
        None,
        Parameters(),
        Parameters(headers={"foo": "bar2"}),
        Parameters(headers={"bar": "foo"}),
    ],
)
def test_insert_headers(parameters: Parameters):
    inference_request = InferenceRequest(inputs=[], parameters=parameters)
    headers = {"foo": "bar", "hello": "world"}
    insert_headers(inference_request, headers)

    assert inference_request.parameters is not None
    assert inference_request.parameters.headers == headers


@pytest.mark.parametrize(
    "parameters, expected",
    [
        (None, None),
        (Parameters(), None),
        (Parameters(headers={}), {}),
        (Parameters(headers={"foo": "bar"}), {"foo": "bar"}),
    ],
)
def test_extract_headers(parameters: Parameters, expected: Dict[str, str]):
    inference_response = InferenceResponse(
        model_name="foo", outputs=[], parameters=parameters
    )
    headers = extract_headers(inference_response)

    assert headers == expected
    if inference_response.parameters:
        assert inference_response.parameters.headers is None


def test_async_manager_defaults():
    async_mgr = AsyncManager()
    assert async_mgr.event_loop_backend == EventLoopBackend.UVLOOP

    async def in_event_loop():
        loop = asyncio.get_running_loop()
        import uvloop

        assert isinstance(loop, uvloop.Loop)

    async_mgr.run(in_event_loop())


def test_async_manager_signal_handlers():
    calls = 0
    signal_to_test = signal.SIGUSR1

    def sgn_handler():
        nonlocal calls
        calls += 1

    def loop_signal_handler_config(loop):
        nonlocal signal_to_test
        loop.add_signal_handler(signal_to_test, sgn_handler)

    async def in_event_loop():
        nonlocal calls
        pid = os.getpid()
        await asyncio.sleep(2)
        os.kill(pid, signal_to_test)
        await asyncio.sleep(1)
        assert calls == 1

    async_mgr = AsyncManager(loop_signal_handler_config)
    async_mgr.run(in_event_loop())
