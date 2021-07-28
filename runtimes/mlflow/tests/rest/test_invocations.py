import pytest

from typing import Union


@pytest.mark.parametrize("content_type", ["", None, "application/pdf"])
def test_invocations_invalid_content_type(rest_client, content_type: str):
    response = rest_client.post("/invocations", headers={"Content-Type": content_type})

    assert response.status_code == 400


@pytest.mark.parametrize(
    "content_type, payload",
    [
        ("application/json", {"columns": ["a"], "data": [1, 2, 3]}),
        ("application/json; format=pandas-records", [{"a": 1}, {"a": 2}, {"a": 3}]),
        ("application/json", {"instances": [1, 2, 3]}),
        ("application/json", {"inputs": [1, 2, 3]}),
    ],
)
def test_invocations(rest_client, content_type: str, payload: Union[list, dict]):
    response = rest_client.post(
        "/invocations", headers={"Content-Type": content_type}, json=payload
    )

    assert response.status_code == 200

    y_pred = response.json()
    assert isinstance(y_pred, list)
    assert len(y_pred) == 3
