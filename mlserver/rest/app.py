from fastapi import FastAPI
from fastapi.routing import APIRoute

from .endpoints import Endpoints

from ..settings import Settings
from ..handlers import DataPlane


def create_app(settings: Settings, data_plane: DataPlane) -> FastAPI:
    endpoints = Endpoints(data_plane)
    routes = [APIRoute("/v2/health/live", endpoints.live)]

    app = FastAPI(debug=settings.debug, routes=routes)

    return app
