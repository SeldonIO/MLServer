from typing import Callable
from fastapi import FastAPI, Request, Response
from fastapi.routing import APIRoute as FastAPIRoute
from fastapi.responses import ORJSONResponse

from .endpoints import Endpoints, ModelRepositoryEndpoints
from .requests import ORJSONRequest
from .errors import _EXCEPTION_HANDLERS

from ..settings import Settings
from ..handlers import DataPlane, ModelRepositoryHandlers


class APIRoute(FastAPIRoute):
    """
    Custom route to use ORJSONRequest handler.
    """

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request = ORJSONRequest(request.scope, request.receive)
            return await original_route_handler(request)

        return custom_route_handler


def create_app(
    settings: Settings,
    data_plane: DataPlane,
    model_repository_handlers: ModelRepositoryHandlers,
) -> FastAPI:
    endpoints = Endpoints(data_plane)
    model_repository_endpoints = ModelRepositoryEndpoints(model_repository_handlers)

    routes = [
        # Model ready
        APIRoute(
            "/v2/models/{model_name}/ready",
            endpoints.model_ready,
        ),
        APIRoute(
            "/v2/models/{model_name}/versions/{model_version}/ready",
            endpoints.model_ready,
        ),
        # Model infer
        APIRoute(
            "/v2/models/{model_name}/infer",
            endpoints.infer,
            methods=["POST"],
        ),
        APIRoute(
            "/v2/models/{model_name}/versions/{model_version}/infer",
            endpoints.infer,
            methods=["POST"],
        ),
        # Model metadata
        APIRoute(
            "/v2/models/{model_name}",
            endpoints.model_metadata,
        ),
        APIRoute(
            "/v2/models/{model_name}/versions/{model_version}",
            endpoints.model_metadata,
        ),
        # Liveness and readiness
        APIRoute("/v2/health/live", endpoints.live),
        APIRoute("/v2/health/ready", endpoints.ready),
        # Server metadata
        APIRoute(
            "/v2",
            endpoints.metadata,
        ),
    ]

    routes += [
        # Model Repository API
        APIRoute(
            "/v2/repository/index",
            model_repository_endpoints.index,
            methods=["POST"],
        ),
        APIRoute(
            "/v2/repository/models/{model_name}/load",
            model_repository_endpoints.load,
            methods=["POST"],
        ),
        APIRoute(
            "/v2/repository/models/{model_name}/unload",
            model_repository_endpoints.unload,
            methods=["POST"],
        ),
    ]

    app = FastAPI(
        debug=settings.debug,
        routes=routes,  # type: ignore
        default_response_class=ORJSONResponse,
        exception_handlers=_EXCEPTION_HANDLERS,  # type: ignore
    )

    return app
