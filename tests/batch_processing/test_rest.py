import pytest
import json

from mlserver.types import InferenceResponse
from mlserver.batch_processing import process_batch
from mlserver.settings import Settings
from mlserver.types.dataplane import InferenceRequest
from tests.batch_processing.conftest import single_input

from ..utils import RESTClient



async def test_single(rest_client: RESTClient, settings: Settings, single_input: str):
    model_name = "sum-model"
    url = f"{settings.host}:{settings.http_port}"
    await rest_client.wait_until_ready()

    # inference_request = InferenceRequest.parse_file(single_input)
    # response = await rest_client.infer(model_name, inference_request)

    await process_batch(model_name, url, 1, True, single_input, "/tmp/output.txt", "debug", False)

    with open("/tmp/output.txt") as f:
        response = json.load(f)

    assert response["outputs"][0]["data"][0] == 6

async def test_single_with_id(rest_client: RESTClient, settings: Settings, single_input_with_id: str):
    model_name = "sum-model"
    url = f"{settings.host}:{settings.http_port}"
    await rest_client.wait_until_ready()

    # inference_request = InferenceRequest.parse_file(single_input)
    # response = await rest_client.infer(model_name, inference_request)

    await process_batch(model_name, url, 1, True, single_input_with_id, "/tmp/output.txt", "debug", False)

    with open("/tmp/output.txt") as f:
        response = json.load(f)

    assert response["outputs"][0]["data"][0] == 6
    assert response["id"] == "my-test-id"
