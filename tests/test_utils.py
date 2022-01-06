import pytest

from typing import Dict, Optional
from unittest.mock import patch

from mlserver.utils import get_model_uri, extract_headers, insert_headers
from mlserver.types import InferenceRequest, InferenceResponse, Parameters
from mlserver.settings import ModelSettings, ModelParameters


@pytest.mark.parametrize(
    "uri, source, expected",
    [
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
    ],
)
async def test_get_model_uri(uri: str, source: Optional[str], expected: str):
    model_settings = ModelSettings(parameters=ModelParameters(uri=uri))
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
