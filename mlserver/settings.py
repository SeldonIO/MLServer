import sys
import os
import json
import importlib

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseSettings, PyObject, Extra, Field
from contextlib import contextmanager

from .version import __version__
from .types import MetadataTensor

ENV_FILE_SETTINGS = ".env"
ENV_PREFIX_SETTINGS = "MLSERVER_"
ENV_PREFIX_MODEL_SETTINGS = "MLSERVER_MODEL_"

DEFAULT_PARALLEL_WORKERS = 1


@contextmanager
def _extra_sys_path(extra_path: str):
    sys.path.insert(0, extra_path)

    yield

    sys.path.remove(extra_path)


def _reload_module(obj: dict):
    import_path = obj.get("implementation", None)
    if not import_path:
        return

    module_path, _, _ = import_path.rpartition(".")
    module = importlib.import_module(module_path)
    importlib.reload(module)


class CORSSettings(BaseSettings):
    class Config:
        env_file = ENV_FILE_SETTINGS
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
        env_file = ENV_FILE_SETTINGS
        env_prefix = ENV_PREFIX_SETTINGS

    debug: bool = True

    parallel_workers: int = DEFAULT_PARALLEL_WORKERS
    """When parallel inference is enabled, number of workers to run inference
    across."""

    parallel_workers_timeout: int = 5
    """Grace timeout to wait until the workers shut down when stopping MLServer."""

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

    # HTTP Server settings
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
    `None` to disable it.
    """

    metrics_port: int = 8082
    """
    Port used to expose metrics endpoint.
    """

    metrics_rest_server_prefix: str = "rest_server"
    """
    Metrics rest server string prefix to be exported.
    """

    # Logging settings
    logging_settings: Optional[Union[str, Dict]] = None
    """Path to logging config file or dictionary configuration."""

    # Kakfa Server settings
    kafka_enabled: bool = False
    kafka_servers: str = "localhost:9092"
    kafka_topic_input: str = "mlserver-input"
    kafka_topic_output: str = "mlserver-output"

    # Custom server settings
    _custom_rest_server_settings: Optional[dict] = None
    _custom_metrics_server_settings: Optional[dict] = None
    _custom_grpc_server_settings: Optional[dict] = None


class ModelParameters(BaseSettings):
    """
    Parameters that apply only to a particular instance of a model.
    This can include things like model weights, or arbitrary ``extra``
    parameters particular to the underlying inference runtime.
    The main difference with respect to ``ModelSettings`` is that parameters
    can change on each instance (e.g. each version) of the model.
    """

    class Config:
        extra = Extra.allow
        env_file = ENV_FILE_SETTINGS
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
        env_file = ENV_FILE_SETTINGS
        env_prefix = ENV_PREFIX_MODEL_SETTINGS
        underscore_attrs_are_private = True

    # Source points to the file where model settings were loaded from
    _source: Optional[str] = None

    @classmethod
    def parse_file(cls, path: str) -> "ModelSettings":  # type: ignore
        with open(path, "r") as f:
            obj = json.load(f)
            obj["_source"] = path
            return cls.parse_obj(obj)

    @classmethod
    def parse_obj(cls, obj: Any) -> "ModelSettings":
        source = obj.pop("_source", None)
        if not source:
            return super().parse_obj(obj)

        model_folder = os.path.dirname(source)
        with _extra_sys_path(model_folder):
            _reload_module(obj)
            model_settings = super().parse_obj(obj)
            model_settings._source = source
            return model_settings

    @property
    def version(self) -> Optional[str]:
        params = self.parameters
        if params is not None:
            return params.version
        return None

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
    parallel_workers: Optional[int] = Field(
        None,
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
    implementation: PyObject
    """*Python path* to the inference runtime to use to serve this model (e.g.
    ``mlserver_sklearn.SKLearnModel``)."""

    # Model parameters are meant to be set directly by the MLServer runtime.
    # However, it's also possible to override them manually.
    parameters: Optional[ModelParameters] = None
    """Extra parameters for each instance of this model."""
