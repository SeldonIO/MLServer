import pytest
import asyncio
import platform

from typing import Dict, Optional
from unittest.mock import patch

from mlserver.utils import (
    get_model_uri,
    extract_headers,
    insert_headers,
    install_uvloop_event_loop,
)
from mlserver.model import MLModel
from mlserver.types import InferenceRequest, InferenceResponse, Parameters
from mlserver.settings import ModelSettings, ModelParameters

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


def _check_uvloop_availability():
    avail = True
    try:
        import uvloop  # noqa: F401
    except ImportError:  # pragma: no cover
        avail = False
    return avail


def test_uvloop_auto_install():
    uvloop_available = _check_uvloop_availability()
    install_uvloop_event_loop()
    policy = asyncio.get_event_loop_policy()

    if uvloop_available:
        assert type(policy).__module__.startswith("uvloop")
    else:
        if platform.system() == "Windows":
            assert isinstance(policy, asyncio.WindowsProactorEventLoopPolicy)
        elif platform.python_implementation() != "CPython":
            assert isinstance(policy, asyncio.DefaultEventLoopPolicy)
