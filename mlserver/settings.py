from typing import List, Optional
from pydantic import BaseSettings, PyObject

from .version import __version__
from .types import MetadataTensor

ENV_PREFIX_SETTINGS = "MLSERVER_"
ENV_PREFIX_MODEL_SETTINGS = "MLSERVER_MODEL_"


class Settings(BaseSettings):
    class Config:
        env_prefix = ENV_PREFIX_SETTINGS

    debug: bool = True

    # Model repository folder
    model_repository_root: str = "."
    load_models_at_startup: bool = True

    # Server metadata
    server_name: str = "mlserver"
    server_version: str = __version__
    extensions: List[str] = []

    # Server settings
    host: str = "0.0.0.0"
    http_port: int = 8080
    grpc_port: int = 8081
    grpc_workers: int = 10


class ModelParameters(BaseSettings):
    """
    Parameters that apply only to a particular instance of a model.
    This can include things like model weights.
    The main difference with respect to ModelSettings is that parameters can
    change on each instance (e.g. each version) of the model.
    """

    class Config:
        env_prefix = ENV_PREFIX_MODEL_SETTINGS

    uri: Optional[str] = None
    version: Optional[str] = None
    format: Optional[str] = None
    extra: Optional[dict] = {}


class ModelSettings(BaseSettings):
    class Config:
        env_prefix = ENV_PREFIX_MODEL_SETTINGS

    name: str = ""

    # Model metadata
    platform: str = ""
    versions: Optional[List[str]] = []
    inputs: Optional[List[MetadataTensor]] = []
    outputs: Optional[List[MetadataTensor]] = []

    # Parallel settings
    parallel_workers: Optional[int] = 4

    # Custom model class implementation
    implementation: PyObject = "mlserver.model.MLModel"  # type: ignore

    # Model parameters are meant to be set directly by the MLServer runtime.
    # However, it's also possible to override them manually.
    parameters: Optional[ModelParameters] = None
