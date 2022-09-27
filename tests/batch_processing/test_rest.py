import os
from uuid import UUID
import pytest
import json

from mlserver.batch_processing import process_batch
from mlserver.settings import Settings
from tempfile import TemporaryDirectory


from ..utils import RESTClient


async def test_single(
    tmp_dir: TemporaryDirectory,
    rest_client: RESTClient,
    settings: Settings,
    single_input: str,
):
    await rest_client.wait_until_ready()
    model_name = "sum-model"
    url = f"{settings.host}:{settings.http_port}"
    output_file = os.path.join(tmp_dir.name, "output.txt")

    await process_batch(
        model_name=model_name,
        url=url,
        workers=1,
        input_data_path=single_input,
        output_data_path=output_file,
        binary_data=False,
        transport="rest",
        use_ssl=False,
        insecure=False,
        verbose=True,
        extra_verbose=True,
    )

    with open(output_file) as f:
        response = json.load(f)

    assert response["outputs"][0]["data"][0] == 6
    assert response["id"] is not None and response["id"] != ""
    assert response["parameters"]["batch_index"] == 0
    try:
        _ = UUID(response["id"])
    except ValueError:
        raise RuntimeError(f"Response id is not a valid UUID; got {response['id']}")


async def test_many(
    tmp_dir: TemporaryDirectory,
    rest_client: RESTClient,
    settings: Settings,
    many_input: str,
):
    await rest_client.wait_until_ready()
    model_name = "sum-model"
    url = f"{settings.host}:{settings.http_port}"
    output_file = os.path.join(tmp_dir.name, "output.txt")

    await process_batch(
        model_name=model_name,
        url=url,
        workers=1,
        input_data_path=many_input,
        output_data_path=output_file,
        binary_data=False,
        transport="rest",
        use_ssl=False,
        insecure=False,
        verbose=True,
        extra_verbose=True,
    )

    with open(output_file) as f:
        lines = f.readlines()
        responses = [json.loads(line) for line in lines]

    for response in responses:
        assert (
            response["outputs"][0]["data"][0]
            == response["parameters"]["batch_index"] + 1
        )
        assert response["id"] is not None and response["id"] != ""
        try:
            _ = UUID(response["id"])
        except ValueError:
            raise RuntimeError(f"Response id is not a valid UUID; got {response['id']}")


async def test_single_with_id(
    tmp_dir: TemporaryDirectory,
    rest_client: RESTClient,
    settings: Settings,
    single_input_with_id: str,
):
    await rest_client.wait_until_ready()
    model_name = "sum-model"
    url = f"{settings.host}:{settings.http_port}"
    output_file = os.path.join(tmp_dir.name, "output.txt")

    await process_batch(
        model_name=model_name,
        url=url,
        workers=1,
        input_data_path=single_input_with_id,
        output_data_path=output_file,
        binary_data=False,
        transport="rest",
        use_ssl=False,
        insecure=False,
        verbose=True,
        extra_verbose=True,
    )

    with open(output_file) as f:
        response = json.load(f)

    assert response["outputs"][0]["data"][0] == 6
    assert response["id"] == "my-test-id"
