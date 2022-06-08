import pytest

from mlserver.settings import Settings, ModelSettings
from mlserver.types import InferenceRequest, InferenceResponse
from mlserver.cloudevents import CloudEventsMiddleware, CloudEventsTypes


@pytest.fixture
def cloudevents_middleware(settings: Settings) -> CloudEventsMiddleware:
    return CloudEventsMiddleware(settings=settings)


def test_request_headers(
    cloudevents_middleware: CloudEventsMiddleware,
    inference_request: InferenceRequest,
    sum_model_settings: ModelSettings,
):
    request_with_headers = cloudevents_middleware.request_middleware(
        inference_request, sum_model_settings
    )

    assert request_with_headers.parameters is not None
    assert request_with_headers.parameters.headers is not None

    headers = request_with_headers.parameters.headers
    assert "Ce-Modelid" in headers
    assert headers["Ce-Modelid"] == sum_model_settings.name
    assert "Ce-Type" in headers
    assert headers["Ce-Type"] == CloudEventsTypes.Request


def test_response_headers(
    cloudevents_middleware: CloudEventsMiddleware,
    inference_response: InferenceResponse,
    sum_model_settings: ModelSettings,
):
    response_with_headers = cloudevents_middleware.response_middleware(
        inference_response, sum_model_settings
    )

    assert response_with_headers.parameters is not None
    assert response_with_headers.parameters.headers is not None

    headers = response_with_headers.parameters.headers
    assert "Ce-Modelid" in headers
    assert headers["Ce-Modelid"] == sum_model_settings.name
    assert "Ce-Type" in headers
    assert headers["Ce-Type"] == CloudEventsTypes.Response
