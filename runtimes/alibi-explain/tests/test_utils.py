from typing import Dict
from functools import wraps
from unittest.mock import patch

import pytest
from fastapi import FastAPI

from mlserver_alibi_explain.common import (
    import_and_get_class,
    remote_metadata,
    construct_metadata_url,
)
from mlserver_alibi_explain.alibi_dependency_reference import _TAG_TO_RT_IMPL
from fastapi.testclient import TestClient


@pytest.mark.parametrize("explainer_reference", _TAG_TO_RT_IMPL.values())
def test_can_load_runtime_impl(explainer_reference):
    import_and_get_class(explainer_reference.runtime_class)
    import_and_get_class(explainer_reference.alibi_class)


def remove_kwarg(func, to_remove):
    @wraps(func)
    def _f(*args, **kwargs):
        kwargs.pop(to_remove, None)
        return func(*args, **kwargs)

    return _f


class _TestClientWrapper:
    def __init__(self, data: Dict):
        self.response = data

    def get_test_client(self):
        app = FastAPI()

        @app.get("/")
        async def metadata() -> Dict:
            return self.response

        test_client = TestClient(app)
        # NOTE: FastAPI / Starlette no longer expose the `verify` flag on the
        # `.get()` method, so let's pop it before calling the actual `.get()`
        # See https://github.com/encode/starlette/pull/1376
        test_client.get = remove_kwarg(test_client.get, "verify")
        return test_client


@pytest.mark.parametrize(
    "data, expected_input_name, expected_name",
    [
        (
            {
                "name": "cifar10",
                "versions": ["1"],
                "platform": "tensorflow_savedmodel",
                "inputs": [
                    {"name": "input_1", "datatype": "FP32", "shape": [-1, 32, 32, 3]}
                ],
                "outputs": [{"name": "fc10", "datatype": "FP32", "shape": [-1, 10]}],
            },
            "input_1",
            "cifar10",
        ),
        (
            {
                "name": "classifier",
                "versions": [],
                "platform": "",
                "inputs": [],
                "outputs": [],
            },
            None,
            "classifier",
        ),
    ],
)
def test_remote_metadata__smoke(data, expected_input_name, expected_name):
    with patch("mlserver_alibi_explain.common.requests") as mock_requests:
        test_client = _TestClientWrapper(data)

        mock_requests.get = test_client.get_test_client().get
        result = remote_metadata("/", ssl_verify_path="")

        if result.inputs:
            assert result.inputs[0].name == expected_input_name
        assert result.name == expected_name


@pytest.mark.parametrize(
    "infer_url, metadata_url",
    [
        ("http://v2/model/infer", "http://v2/model"),
        ("http://v2/infer/infer", "http://v2/infer"),
        ("http://v2/model", "http://v2/model"),
    ],
)
def test_metadata_url_from_infer_url(infer_url, metadata_url):
    assert construct_metadata_url(infer_url) == metadata_url
