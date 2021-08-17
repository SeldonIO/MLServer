import pytest
import numpy as np
from typing import Union


@pytest.mark.parametrize("content_type", ["", None, "application/pdf"])
def test_invocations_invalid_content_type(rest_client, content_type: str):
    response = rest_client.post("/invocations", headers={"Content-Type": content_type})

    assert response.status_code == 400


@pytest.mark.parametrize(
    "content_type, payload",
    [
        ("application/json", {"columns": [i for i in range(28*28)], "data": np.random.randn(1, 28*28).tolist()}),
    ],
)
def test_invocations(rest_client, content_type: str, payload: Union[list, dict]):
    response = rest_client.post(
        "/invocations", headers={"Content-Type": content_type}, json=payload
    )

    assert response.status_code == 200

    y_pred = response.json()
    assert isinstance(y_pred, list)
