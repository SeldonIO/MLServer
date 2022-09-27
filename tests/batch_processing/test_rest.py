from uuid import UUID
import pytest
import json

from mlserver.batch_processing import process_batch
from mlserver.settings import Settings


from ..utils import RESTClient


async def test_single(rest_client: RESTClient, settings: Settings, single_input: str):
    model_name = "sum-model"
    url = f"{settings.host}:{settings.http_port}"
    await rest_client.wait_until_ready()

    await process_batch(
        model_name=model_name,
        url=url,
        workers=1,
        input_data_path=single_input,
        output_data_path="/tmp/output.txt",
        binary_data=False,
        transport="rest",
        use_ssl=False,
        insecure=False,
        verbose=True,
        extra_verbose=True,
    )

    with open("/tmp/output.txt") as f:
        response = json.load(f)

    assert response["outputs"][0]["data"][0] == 6
    assert response["id"] is not None and response["id"] != ""
    try:
        _ = UUID(response["id"])
    except ValueError:
        raise RuntimeError(f"Response id is not a valid UUID; got {response['id']}")


async def test_single_with_id(
    rest_client: RESTClient, settings: Settings, single_input_with_id: str
):
    model_name = "sum-model"
    url = f"{settings.host}:{settings.http_port}"
    await rest_client.wait_until_ready()

    await process_batch(
        model_name=model_name,
        url=url,
        workers=1,
        input_data_path=single_input_with_id,
        output_data_path="/tmp/output.txt",
        binary_data=False,
        transport="rest",
        use_ssl=False,
        insecure=False,
        verbose=True,
        extra_verbose=True,
    )

    with open("/tmp/output.txt") as f:
        response = json.load(f)

    assert response["outputs"][0]["data"][0] == 6
    assert response["id"] == "my-test-id"
