from fastapi.requests import Request
from fastapi.responses import Response, HTMLResponse, StreamingResponse
from fastapi.openapi.docs import get_swagger_ui_html

from typing import AsyncIterator, Optional

from ..types import (
    MetadataModelResponse,
    MetadataServerResponse,
    InferenceRequest,
    InferenceResponse,
    RepositoryIndexRequest,
    RepositoryIndexResponse,
)
from ..handlers import DataPlane, ModelRepositoryHandlers
from ..utils import insert_headers, extract_headers

from .responses import ServerSentEvent
from .openapi import get_openapi_schema, get_model_schema_uri, get_model_schema
from .utils import to_status_code


class Endpoints:
    """
    Implementation of REST endpoints.
    These take care of the REST/HTTP-specific things and then delegate the
    business logic to the internal handlers.
    """

    def __init__(self, data_plane: DataPlane):
        self._data_plane = data_plane

    async def live(self) -> Response:
        is_live = await self._data_plane.live()
        return Response(status_code=to_status_code(is_live))

    async def ready(self) -> Response:
        is_ready = await self._data_plane.ready()
        return Response(status_code=to_status_code(is_ready))

    async def openapi(self) -> dict:
        return get_openapi_schema()

    async def docs(self) -> HTMLResponse:
        openapi_url = "/v2/docs/dataplane.json"
        title = "MLServer API Docs"
        return get_swagger_ui_html(openapi_url=openapi_url, title=title)

    async def model_openapi(
        self, model_name: str, model_version: Optional[str] = None
    ) -> dict:
        # NOTE: Right now, we use the `model_metadata` method to check that the
        # model exists.
        # In the future, we will use this metadata to fill in more model
        # details in the schema (e.g. expected inputs, etc.).
        await self._data_plane.model_metadata(model_name, model_version)
        return get_model_schema(model_name, model_version)

    async def model_docs(
        self, model_name: str, model_version: Optional[str] = None
    ) -> HTMLResponse:
        # NOTE: Right now, we use the `model_metadata` method to check that the
        # model exists.
        # In the future, we will use this metadata to fill in more model
        # details in the schema (e.g. expected inputs, etc.).
        await self._data_plane.model_metadata(model_name, model_version)
        openapi_url = get_model_schema_uri(model_name, model_version)

        title = f"MLServer API Docs - {model_name}"
        if model_version:
            title = f"{title} ({model_version})"

        return get_swagger_ui_html(openapi_url=openapi_url, title=title)

    async def model_ready(
        self, model_name: str, model_version: Optional[str] = None
    ) -> Response:
        is_ready = await self._data_plane.model_ready(model_name, model_version)
        return Response(status_code=to_status_code(is_ready))

    async def metadata(self) -> MetadataServerResponse:
        return await self._data_plane.metadata()

    async def model_metadata(
        self, model_name: str, model_version: Optional[str] = None
    ) -> MetadataModelResponse:
        return await self._data_plane.model_metadata(model_name, model_version)

    async def infer(
        self,
        raw_request: Request,
        raw_response: Response,
        payload: InferenceRequest,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> InferenceResponse:

        request_headers = dict(raw_request.headers)
        insert_headers(payload, request_headers)

        inference_response = await self._data_plane.infer(
            payload, model_name, model_version
        )
        response_headers = extract_headers(inference_response)

        if response_headers:
            raw_response.headers.update(response_headers)

        return inference_response

    async def infer_stream(
        self,
        raw_request: Request,
        raw_response: Response,
        payload: InferenceRequest,
        model_name: str,
        model_version: Optional[str] = None,
    ) -> StreamingResponse:

        request_headers = dict(raw_request.headers)
        insert_headers(payload, request_headers)

        async def payloads_async_iter(
            payload: InferenceRequest,
        ) -> AsyncIterator[InferenceRequest]:
            yield payload

        payloads = payloads_async_iter(payload)
        infer_stream = self._data_plane.infer_stream(
            payloads, model_name, model_version
        )

        sse_stream = _as_sse(infer_stream)
        return StreamingResponse(content=sse_stream, media_type="text/event-stream")


async def _as_sse(
    infer_stream: AsyncIterator[InferenceResponse],
) -> AsyncIterator[bytes]:
    """
    Helper to convert all the responses coming out of a generator to a
    Server-Sent Event object.
    """
    async for inference_response in infer_stream:
        # TODO: How should we send headers back?
        # response_headers = extract_headers(inference_response)
        yield ServerSentEvent(inference_response).encode()


class ModelRepositoryEndpoints:
    def __init__(self, handlers: ModelRepositoryHandlers):
        self._handlers = handlers

    async def index(self, payload: RepositoryIndexRequest) -> RepositoryIndexResponse:
        return await self._handlers.index(payload)

    async def load(self, model_name: str) -> Response:
        loaded = await self._handlers.load(name=model_name)
        return Response(status_code=to_status_code(loaded))

    async def unload(self, model_name: str) -> Response:
        unloaded = await self._handlers.unload(name=model_name)
        return Response(status_code=to_status_code(unloaded))
