import pytest

from typing import Optional, Union


@pytest.mark.parametrize("content_type", ["", None, "application/pdf"])
async def test_invocations_invalid_content_type(
    rest_client, content_type: Optional[str]
):
    headers = {}
    if content_type is not None:
        headers = {"Content-Type": content_type}

    response = await rest_client.post("/invocations", headers=headers)

    assert response.status_code == 400


@pytest.mark.parametrize(
    "content_type, payload",
    [
        ("application/json", {"instances": [1, 2, 3]}),
        ("application/json", {"inputs": [1, 2, 3]}),
        ("application/json", {"inputs": {"foo": [1, 2, 3]}}),
    ],
)
async def test_invocations_tensor(
    rest_client, content_type: str, payload: Union[list, dict]
):
    response = await rest_client.post(
        "/invocations", headers={"Content-Type": content_type}, json=payload
    )

    assert response.status_code == 200

    res = response.json()
    assert "predictions" in res

    y_pred = res["predictions"]
    assert isinstance(y_pred, list)
    assert len(y_pred) == 3


@pytest.mark.parametrize(
    "content_type, payload",
    [
        (
            "application/json",
            {"dataframe_split": {"columns": ["foo"], "data": [1, 2, 3]}},
        ),
        (
            "application/json",
            {"dataframe_records": [{"foo": 1}, {"foo": 2}, {"foo": 3}]},
        ),
    ],
)
async def test_invocations_dataframe(
    rest_client, content_type: str, payload: Union[list, dict]
):
    response = await rest_client.post(
        "/invocations", headers={"Content-Type": content_type}, json=payload
    )

    assert response.status_code == 200

    res = response.json()
    assert "predictions" in res

    y_pred = res["predictions"]
    assert isinstance(y_pred, list)
    assert len(y_pred) == 3
