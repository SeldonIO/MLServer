import pytest

from mlserver.types import InferenceRequest


@pytest.mark.parametrize("content_type", ["", None, "application/pdf"])
def test_invocations_invalid_content_type(rest_client, content_type: str):
    response = rest_client.post("/invocations", headers={"Content-Type": content_type})

    assert response.status_code == 400
