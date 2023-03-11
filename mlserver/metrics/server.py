import uvicorn
import os

from typing import Optional, TYPE_CHECKING

from fastapi import FastAPI

from ..settings import Settings
from .logging import logger
from .prometheus import PrometheusEndpoint, stop_metrics

if TYPE_CHECKING:
    from ..parallel import Worker


class _NoSignalServer(uvicorn.Server):
    def install_signal_handlers(self):
        pass


class MetricsServer:
    def __init__(self, settings: Settings):
        self._settings = settings
        self._endpoint = PrometheusEndpoint(settings)
        self._app = self._get_app()

    def _get_app(self):
        app = FastAPI(debug=self._settings.debug)
        app.add_route(self._settings.metrics_endpoint, self._endpoint.handle_metrics)
        return app

    async def on_worker_stop(self, worker: "Worker") -> None:
        if not worker.pid:
            return

        # NOTE: If a worker gets restarted (instead of regular shutdown), we may
        # not want to remove old files to keep counts intact
        await stop_metrics(self._settings, worker.pid)

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

        if self._settings.logging_settings:
            # If not None, use ours. Otherwise, let Uvicorn fall back on its
            # own config.
            kwargs.update({"log_config": self._settings.logging_settings})

        return uvicorn.Config(self._app, **kwargs)

    async def stop(self, sig: Optional[int] = None):
        await stop_metrics(self._settings, os.getpid())
        self._server.handle_exit(sig=sig, frame=None)
