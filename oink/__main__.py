"""
Starts an inference server.
"""
import uvicorn

from .rest import create_app
from .settings import Settings
from .handlers import DataPlane

if __name__ == "__main__":
    settings = Settings()
    data_plane = DataPlane()

    app = create_app(settings, data_plane)
    uvicorn.run(app, port=settings.http_port)
