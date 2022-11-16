import uvicorn

from fastapi import FastAPI
from starlette_exporter import handle_metrics

from ..settings import Settings
from .logging import logger
from typing import Optional


class _NoSignalServer(uvicorn.Server):
    def install_signal_handlers(self):
        pass


class MetricsServer:
    def __init__(self, settings: Settings):
        self._settings = settings
        self._app = self._get_app()

    def _get_app(self):
        app = FastAPI(debug=self._settings.debug)
        app.add_route(self._settings.metrics_endpoint, handle_metrics)
        return app

    async def start(self):
        cfg = self._get_config()
        self._server = _NoSignalServer(cfg)

        metrics_server = f"http://{self._settings.host}:{self._settings.metrics_port}"
        logger.info(f"Metrics server running on {metrics_server}")
        logger.info(
            "Prometheus scraping endpoint can be accessed on "
            f"{metrics_server}{self._settings.metrics_endpoint}"
        )
        await self._server.serve()

    def _get_config(self):
        kwargs = {}

        if self._settings._custom_metrics_server_settings:
            logger.warning(
                "REST custom configuration is out of support. Use as your own risk"
            )
            kwargs.update(self._settings._custom_metrics_server_settings)

        kwargs.update(
            {
                "host": self._settings.host,
                "port": self._settings.metrics_port,
                "access_log": self._settings.debug,
            }
        )

        # TODO: we want to disable logger unless debug is enabled (otherwise,
        # prom reqs can be spammy)
        return uvicorn.Config(self._app, **kwargs)

    async def stop(self, sig: Optional[int] = None):
        self._server.handle_exit(sig=sig, frame=None)
