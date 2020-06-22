from typing import List
from pydantic import BaseSettings

from .version import __version__


class Settings(BaseSettings):
    debug: bool = True

    # Server metadata
    server_name: str = "mlserver"
    server_version: str = __version__
    extensions: List[str] = []

    # Server settings
    http_port: int = 8080
    grpc_port: int = 8081
    grpc_workers: int = 10
