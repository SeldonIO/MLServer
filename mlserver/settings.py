import multiprocessing

from typing import List, Optional
from pydantic import BaseSettings, PyObject, Field

from .version import __version__
from .types import MetadataTensor

ENV_PREFIX_SETTINGS = "MLSERVER_"
ENV_PREFIX_MODEL_SETTINGS = "MLSERVER_MODEL_"

DEFAULT_PARALLEL_WORKERS = multiprocessing.cpu_count()


class CORSSettings(BaseSettings):
    class Config:
        env_prefix = ENV_PREFIX_SETTINGS

    allow_origins: Optional[List[str]] = []
    """
    A list of origins that should be permitted to make
    cross-origin requests. E.g. ['https://example.org', 'https://www.example.org'].
    You can use ['*'] to allow any origin
    """

    allow_origin_regex: Optional[str] = None
    """
    A regex string to match against origins that
    should be permitted to make cross-origin requests.
    e.g. 'https:\\/\\/.*\\.example\\.org'
    """

    allow_credentials: Optional[bool] = False
    """Indicate that cookies should be supported for cross-origin requests"""

    allow_methods: Optional[List[str]] = ["GET"]
    """A list of HTTP methods that should be allowed for cross-origin requests"""

    allow_headers: Optional[List[str]] = []
    """A list of HTTP request headers that should be supported for
    cross-origin requests"""

    expose_headers: Optional[List[str]] = []
    """Indicate any response headers that should be made accessible to the browser"""

    max_age: Optional[int] = 600
    """Sets a maximum time in seconds for browsers to cache CORS responses"""


class Settings(BaseSettings):
    class Config:
        env_prefix = ENV_PREFIX_SETTINGS

    debug: bool = True

    parallel_workers: int = DEFAULT_PARALLEL_WORKERS
    """When parallel inference is enabled, number of workers to run inference
    across."""

    # Model repository settings
    model_repository_root: str = "."
    """Root of the model repository, where we will search for models."""

    load_models_at_startup: bool = True
    """Flag to load all available models automatically at startup."""

    # Server metadata
    server_name: str = "mlserver"
    """Name of the server."""

    server_version: str = __version__
    """Version of the server."""

    extensions: List[str] = []
    """Server extensions loaded."""

    # Server settings
    host: str = "0.0.0.0"
    """Host where to listen for connections."""

    http_port: int = 8080
    """Port where to listen for HTTP / REST connections."""

    root_path: str = ""
    """Set the ASGI root_path for applications submounted below a given URL path."""

    grpc_port: int = 8081
    """Port where to listen for gRPC connections."""

    grpc_max_message_length: Optional[int] = None
    """Maximum length (i.e. size) of gRPC payloads."""

    # CORS settings
    cors_settings: Optional[CORSSettings] = None

    # Metrics settings
    metrics_endpoint: Optional[str] = "/metrics"
    """
    Endpoint used to expose Prometheus metrics. Alternatively, can be set to
    `None` to disable it
    """

    # Logging settings
    logging_settings: Optional[str] = None
    """Path to logging config file"""


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

    uri: Optional[str] = None
    """
    URI where the model artifacts can be found.
    This path must be either absolute or relative to where MLServer is running.
    """

    version: Optional[str] = None
    """Version of the model."""

    format: Optional[str] = None
    """Format of the model (only available on certain runtimes)."""

    content_type: Optional[str] = None
    """Default content type to use for requests and responses."""

    extra: Optional[dict] = {}
    """Arbitrary settings, dependent on the inference runtime
    implementation."""


class ModelSettings(BaseSettings):
    class Config:
        env_prefix = ENV_PREFIX_MODEL_SETTINGS
        underscore_attrs_are_private = True

    # Source points to the file where model settings were loaded from
    _source: Optional[str] = None

    name: str = ""
    """Name of the model."""

    # Model metadata
    platform: str = ""
    """Framework used to train and serialise the model (e.g. sklearn)."""

    versions: List[str] = []
    """Versions of dependencies used to train the model (e.g.
    sklearn/0.20.1)."""

    inputs: List[MetadataTensor] = []
    """Metadata about the inputs accepted by the model."""

    outputs: List[MetadataTensor] = []
    """Metadata about the outputs returned by the model."""

    # Parallel settings
    parallel_workers: int = Field(
        DEFAULT_PARALLEL_WORKERS,
        deprecated=True,
        description=(
            "Use the `parallel_workers` field the server wide settings instead."
        ),
    )

    warm_workers: bool = Field(
        False,
        deprecated=True,
        description="Inference workers will now always be `warmed up` at start time.",
    )

    # Adaptive Batching settings (disabled by default)
    max_batch_size: int = 0
    """When adaptive batching is enabled, maximum number of requests to group
    together in a single batch."""

    max_batch_time: float = 0.0
    """When adaptive batching is enabled, maximum amount of time (in seconds)
    to wait for enough requests to build a full batch."""

    # Custom model class implementation
    implementation: PyObject = "mlserver.model.MLModel"  # type: ignore
    """*Python path* to the inference runtime to use to serve this model (e.g.
    ``mlserver_sklearn.SKLearnModel``)."""

    # Model parameters are meant to be set directly by the MLServer runtime.
    # However, it's also possible to override them manually.
    parameters: Optional[ModelParameters] = None
    """Extra parameters for each instance of this model."""
