from unittest.mock import patch

import pytest
from fastapi import FastAPI

from mlserver_alibi_explain.common import import_and_get_class, remote_metadata, \
    construct_metadata_url
from mlserver_alibi_explain.alibi_dependency_reference import _TAG_TO_RT_IMPL
from fastapi.testclient import TestClient


@pytest.mark.parametrize("explainer_reference", _TAG_TO_RT_IMPL.values())
def test_can_load_runtime_impl(explainer_reference):
    import_and_get_class(explainer_reference.runtime_class)
    import_and_get_class(explainer_reference.alibi_class)


@pytest.fixture()
def test_client() -> TestClient:
    app = FastAPI()

    @app.get("/")
    async def metadata():
        return {
            "name": "cifar10",
            "versions": ["1"],
            "platform": "tensorflow_savedmodel",
            "inputs": [
                {
                    "name": "input_1",
                    "datatype": "FP32",
                    "shape": [-1, 32, 32, 3]}
            ],
            "outputs": [
                {
                    "name": "fc10",
                    "datatype": "FP32",
                    "shape": [-1, 10]
                }
            ]
        }

    return TestClient(app)


def test_remote_metadata__smoke(test_client):
    with patch("mlserver_alibi_explain.common.requests") as mock_requests:
        mock_requests.get = test_client.get
        result = remote_metadata("/")
        assert result.inputs[0].name == "input_1"
        assert result.name == "cifar10"


@pytest.mark.parametrize(
    "infer_url, metadata_url",
    [
        ("http://v2/model/infer", "http://v2/model"),
        ("http://v2/infer/infer", "http://v2/infer"),
        ("http://v2/model", "http://v2/model"),
    ]
)
def test_metadata_url_from_infer_url(infer_url, metadata_url):
    assert construct_metadata_url(infer_url) == metadata_url
