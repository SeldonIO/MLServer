import uvicorn

from ..settings import Settings
from ..handlers import DataPlane

from .app import create_app


class RESTServer:
    def __init__(self, settings: Settings, data_plane: DataPlane):
        self._settings = settings
        self._data_plane = data_plane
        self._app = create_app(self._settings, self._data_plane)

    def start(self):
        uvicorn.run(
            self._app,
            port=self._settings.http_port,
            #  workers=self._settings.http_workers,
            #  loop="uvloop",
        )
