import uvicorn

from ..settings import Settings
from ..handlers import DataPlane, ModelRepositoryHandlers

from .app import create_app


class _NoSignalServer(uvicorn.Server):
    def install_signal_handlers(self):
        pass


class RESTServer:
    def __init__(
        self,
        settings: Settings,
        data_plane: DataPlane,
        model_repository_handlers: ModelRepositoryHandlers,
    ):
        self._settings = settings
        self._data_plane = data_plane
        self._model_repository_handlers = model_repository_handlers
        self._app = create_app(
            self._settings,
            data_plane=self._data_plane,
            model_repository_handlers=self._model_repository_handlers,
        )

    async def start(self):
        cfg = uvicorn.Config(
            self._app, host=self._settings.host, port=self._settings.http_port
        )
        self._server = _NoSignalServer(cfg)
        await self._server.serve()

    async def stop(self):
        self._server.handle_exit(sig=None, frame=None)
