from typing import List, Optional
from pydantic import BaseSettings

from .version import __version__
from .types import MetadataTensor


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


class ModelSettings(BaseSettings):
    name: str

    # Model metadata
    platform: str = ""
    versions: Optional[List[str]] = []
    inputs: Optional[List[MetadataTensor]] = []
