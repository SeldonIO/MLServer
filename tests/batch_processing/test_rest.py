import os
from uuid import UUID
import json
import pytest

from mlserver.batch_processing import process_batch
from mlserver.settings import Settings
from mlserver import MLModel

from ..utils import RESTClient


async def test_single(
    tmp_path: str,
    rest_client: RESTClient,
    settings: Settings,
    single_input: str,
):
    await rest_client.wait_until_ready()
    model_name = "sum-model"
    url = f"{settings.host}:{settings.http_port}"
    output_file = os.path.join(tmp_path, "output.txt")

    await process_batch(
        model_name=model_name,
        url=url,
        workers=1,
        retries=1,
        input_data_path=single_input,
        output_data_path=output_file,
        binary_data=False,
        batch_size=1,
        transport="rest",
        request_headers={},
        batch_interval=0,
        batch_jitter=0,
        timeout=60,
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


async def test_bytes(
    tmp_path: str,
    echo_model: MLModel,
    rest_client: RESTClient,
    settings: Settings,
    bytes_input: str,
):
    await rest_client.wait_until_ready()
    model_name = "echo-model"
    url = f"{settings.host}:{settings.http_port}"
    output_file = os.path.join(tmp_path, "output.txt")

    await process_batch(
        model_name=model_name,
        url=url,
        workers=1,
        retries=1,
        input_data_path=bytes_input,
        output_data_path=output_file,
        binary_data=False,
        batch_size=1,
        transport="rest",
        request_headers={},
        batch_interval=0,
        batch_jitter=0,
        timeout=60,
        use_ssl=False,
        insecure=False,
        verbose=True,
        extra_verbose=True,
    )

    with open(output_file) as f:
        response = json.load(f)

    assert response["outputs"][0]["data"] == ["a", "b", "c"]
    assert response["id"] is not None and response["id"] != ""
    assert response["parameters"]["batch_index"] == 0
    try:
        _ = UUID(response["id"])
    except ValueError:
        raise RuntimeError(f"Response id is not a valid UUID; got {response['id']}")


async def test_invalid(
    tmp_path: str,
    rest_client: RESTClient,
    settings: Settings,
    invalid_input: str,
):
    await rest_client.wait_until_ready()
    model_name = "sum-model"
    url = f"{settings.host}:{settings.http_port}"
    output_file = os.path.join(tmp_path, "output.txt")

    await process_batch(
        model_name=model_name,
        url=url,
        workers=1,
        retries=1,
        input_data_path=invalid_input,
        output_data_path=output_file,
        binary_data=False,
        batch_size=1,
        transport="rest",
        request_headers={},
        batch_interval=0,
        batch_jitter=0,
        timeout=60,
        use_ssl=False,
        insecure=False,
        verbose=True,
        extra_verbose=True,
    )

    expected_error = {
        "parameters": {"batch_index": 0},
        "error": {
            "status": "preprocessing error",
            "msg": [
                {
                    "type": "missing",
                    "loc": ["inputs", 0, "datatype"],
                    "msg": "Field required",
                    "input": {"name": "input-0", "shape": [1, 3], "data": [1, 2, 3]},
                    "url": "https://errors.pydantic.dev/2.7/v/missing",
                }
            ],
        },
    }

    with open(output_file) as f:
        response = json.load(f)

    assert response == expected_error


async def test_invalid_among_many(
    tmp_path: str,
    rest_client: RESTClient,
    settings: Settings,
    invalid_among_many: str,
):
    await rest_client.wait_until_ready()
    model_name = "sum-model"
    url = f"{settings.host}:{settings.http_port}"
    output_file = os.path.join(tmp_path, "output.txt")

    await process_batch(
        model_name=model_name,
        url=url,
        workers=1,
        retries=1,
        input_data_path=invalid_among_many,
        output_data_path=output_file,
        binary_data=False,
        batch_size=1,
        transport="rest",
        request_headers={},
        batch_interval=0,
        batch_jitter=0,
        timeout=60,
        use_ssl=False,
        insecure=False,
        verbose=True,
        extra_verbose=True,
    )

    expected_error = {
        "parameters": {"batch_index": 2},
        "error": {
            "status": "preprocessing error",
            "msg": [
                {
                    "type": "missing",
                    "loc": ["inputs", 0, "datatype"],
                    "msg": "Field required",
                    "input": {"name": "input-0", "shape": [1, 3], "data": [1, 2, 3]},
                    "url": "https://errors.pydantic.dev/2.7/v/missing",
                }
            ],
        },
    }

    with open(output_file) as f:
        lines = f.readlines()
        responses = [json.loads(line) for line in lines]

    assert len(responses) == 6
    for response in responses:
        if response["parameters"]["batch_index"] == 2:
            assert response == expected_error
            continue
        assert (
            response["outputs"][0]["data"][0]
            == response["parameters"]["batch_index"] + 1
        )
        assert response["id"] is not None and response["id"] != ""
        try:
            _ = UUID(response["id"])
        except ValueError:
            raise RuntimeError(f"Response id is not a valid UUID; got {response['id']}")

        assert response["parameters"]["inference_id"] == response["id"]


@pytest.mark.parametrize("workers", [1, 2, 5, 6])
async def test_many(
    workers: int,
    tmp_path: str,
    rest_client: RESTClient,
    settings: Settings,
    many_input: str,
):
    await rest_client.wait_until_ready()
    model_name = "sum-model"
    url = f"{settings.host}:{settings.http_port}"
    output_file = os.path.join(tmp_path, "output.txt")

    await process_batch(
        model_name=model_name,
        url=url,
        workers=workers,
        retries=1,
        input_data_path=many_input,
        output_data_path=output_file,
        binary_data=False,
        batch_size=1,
        transport="rest",
        request_headers={},
        batch_interval=0,
        batch_jitter=0,
        timeout=60,
        use_ssl=False,
        insecure=False,
        verbose=True,
        extra_verbose=True,
    )

    with open(output_file) as f:
        lines = f.readlines()
        responses = [json.loads(line) for line in lines]

    assert len(responses) == 6
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

        assert response["parameters"]["inference_id"] == response["id"]


@pytest.mark.parametrize("workers", [1, 2, 5, 6])
async def test_many_batch(
    workers: int,
    tmp_path: str,
    rest_client: RESTClient,
    settings: Settings,
    many_input: str,
):
    await rest_client.wait_until_ready()
    model_name = "sum-model"
    url = f"{settings.host}:{settings.http_port}"
    output_file = os.path.join(tmp_path, "output.txt")

    await process_batch(
        model_name=model_name,
        url=url,
        workers=workers,
        retries=1,
        input_data_path=many_input,
        output_data_path=output_file,
        binary_data=False,
        batch_size=3,
        transport="rest",
        request_headers={},
        batch_interval=0,
        batch_jitter=0,
        timeout=60,
        use_ssl=False,
        insecure=False,
        verbose=True,
        extra_verbose=True,
    )

    with open(output_file) as f:
        lines = f.readlines()
        responses = [json.loads(line) for line in lines]

    assert len(responses) == 6
    inference_indices = []
    for response in responses:
        inference_indices.append(response["parameters"]["inference_id"])
        assert (
            response["outputs"][0]["data"][0]
            == response["parameters"]["batch_index"] + 1
        )
        assert response["id"] is not None and response["id"] != ""
        try:
            _ = UUID(response["id"])
        except ValueError:
            raise RuntimeError(f"Response id is not a valid UUID; got {response['id']}")

    # We expect two unique inference indices as we have 6 requests and batch size is 3
    assert len(set(inference_indices)) == 2


async def test_single_with_id(
    tmp_path: str,
    rest_client: RESTClient,
    settings: Settings,
    single_input_with_id: str,
):
    await rest_client.wait_until_ready()
    model_name = "sum-model"
    url = f"{settings.host}:{settings.http_port}"
    output_file = os.path.join(tmp_path, "output.txt")

    await process_batch(
        model_name=model_name,
        url=url,
        workers=1,
        retries=1,
        input_data_path=single_input_with_id,
        output_data_path=output_file,
        binary_data=False,
        batch_size=1,
        transport="rest",
        request_headers={},
        batch_interval=0,
        batch_jitter=0,
        timeout=60,
        use_ssl=False,
        insecure=False,
        verbose=True,
        extra_verbose=True,
    )

    with open(output_file) as f:
        response = json.load(f)

    assert response["outputs"][0]["data"][0] == 6
    assert response["id"] == "my-test-id"
