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

    # Model repository settings
    """Root of the model repository, where we will search for models."""
    model_repository_root: str = "."
    """Flag to load all available models automatically at startup."""
    load_models_at_startup: bool = True

    # Server metadata
    """Name of the server."""
    server_name: str = "mlserver"
    """Version of the server."""
    server_version: str = __version__
    """Server extensions loaded."""
    extensions: List[str] = []

    # Server settings
    """Host where to listen for connections."""
    host: str = "0.0.0.0"
    """Port where to listen for HTTP / REST connections."""
    http_port: int = 8080
    """Port where to listen for gRPC connections."""
    grpc_port: int = 8081
    """Maximum length (i.e. size) of gRPC payloads."""
    grpc_max_message_length: Optional[int] = None


class ModelParameters(BaseSettings):
    """
    Parameters that apply only to a particular instance of a model.
    This can include things like model weights, or arbitrary ``extra``
    parameters particular to the underlying inference runtime.
    The main difference with respect to ``ModelSettings`` is that parameters
    can change on each instance (e.g. each version) of the model.
    """

    class Config:
        env_prefix = ENV_PREFIX_MODEL_SETTINGS

    """
    URI where the model artifacts can be found.
    This path must be either absolute or relative to where MLServer is running.
    """
    uri: Optional[str] = None
    """Version of the model."""
    version: Optional[str] = None
    """Format of the model (only available on certain runtimes)."""
    format: Optional[str] = None
    """Arbitrary settings, dependent on the inference runtime
    implementation."""
    extra: Optional[dict] = {}


class ModelSettings(BaseSettings):
    class Config:
        env_prefix = ENV_PREFIX_MODEL_SETTINGS

    """Name of the model."""
    name: str = ""

    # Model metadata
    """Framework used to train and serialise the model (e.g. sklearn)."""
    platform: str = ""
    """Versions of dependencies used to train the model (e.g.
    sklearn/0.20.1)."""
    versions: List[str] = []
    """Metadata about the inputs accepted by the model."""
    inputs: List[MetadataTensor] = []
    """Metadata about the outputs returned by the model."""
    outputs: List[MetadataTensor] = []

    # Parallel settings
    """When parallel inference is enabled, number of workers to run inference
    across."""
    parallel_workers: int = 4

    # Adaptive Batching settings (disabled by default)
    """When adaptive batching is enabled, maximum number of requests to group
    together in a single batch."""
    max_batch_size: int = 0
    """When adaptive batching is enabled, maximum amount of time (in seconds)
    to wait for enough requests to build a full batch."""
    max_batch_time: float = 0.0

    # Custom model class implementation
    """*Python path* to the inference runtime to use to serve this model (e.g.
    ``mlserver_sklearn.SKLearnModel``)."""
    implementation: PyObject = "mlserver.model.MLModel"  # type: ignore

    # Model parameters are meant to be set directly by the MLServer runtime.
    # However, it's also possible to override them manually.
    """Extra parameters for each instance of this model."""
    parameters: Optional[ModelParameters] = None
