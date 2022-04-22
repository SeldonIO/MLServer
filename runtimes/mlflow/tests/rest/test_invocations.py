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
        ("application/json", {"columns": ["foo"], "data": [1, 2, 3]}),
        (
            "application/json; format=pandas-records",
            [{"foo": 1}, {"foo": 2}, {"foo": 3}],
        ),
        ("application/json", {"instances": [1, 2, 3]}),
        ("application/json", {"inputs": [1, 2, 3]}),
    ],
)
async def test_invocations(rest_client, content_type: str, payload: Union[list, dict]):
    response = await rest_client.post(
        "/invocations", headers={"Content-Type": content_type}, json=payload
    )

    assert response.status_code == 200

    y_pred = response.json()
    assert isinstance(y_pred, list)
    assert len(y_pred) == 1
