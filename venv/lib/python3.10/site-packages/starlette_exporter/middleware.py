""" Middleware for exporting Prometheus metrics using Starlette """
from collections import OrderedDict
import time
import logging
from typing import Any, Callable, List, Mapping, Optional, ClassVar, Dict, Union

from prometheus_client import Counter, Histogram, Gauge
from prometheus_client.metrics import MetricWrapperBase
from starlette.requests import Request
from starlette.routing import Route, Match, Mount
from starlette.types import ASGIApp, Message, Receive, Send, Scope

from . import optional_metrics

logger = logging.getLogger("exporter")


def get_matching_route_path(
    scope: Dict[Any, Any], routes: List[Route], route_name: Optional[str] = None
) -> Optional[str]:
    """
    Find a matching route and return its original path string

    Will attempt to enter mounted routes and subrouters.

    Credit to https://github.com/elastic/apm-agent-python
    """
    for route in routes:
        match, child_scope = route.matches(scope)
        if match == Match.FULL:
            route_name = route.path
            child_scope = {**scope, **child_scope}
            if isinstance(route, Mount) and route.routes:
                child_route_name = get_matching_route_path(
                    child_scope, route.routes, route_name
                )
                if child_route_name is None:
                    route_name = None
                else:
                    route_name += child_route_name
            return route_name
        elif match == Match.PARTIAL and route_name is None:
            route_name = route.path


class PrometheusMiddleware:
    """Middleware that collects Prometheus metrics for each request.
    Use in conjuction with the Prometheus exporter endpoint handler.
    """

    _metrics: ClassVar[Dict[str, MetricWrapperBase]] = {}

    def __init__(
        self,
        app: ASGIApp,
        group_paths: bool = False,
        app_name: str = "starlette",
        prefix: str = "starlette",
        buckets: Optional[List[str]] = None,
        filter_unhandled_paths: bool = False,
        skip_paths: Optional[List[str]] = None,
        optional_metrics: Optional[List[str]] = None,
        always_use_int_status: bool = False,
        labels: Optional[Mapping[str, Union[str, Callable]]] = None,
    ):
        self.app = app
        self.group_paths = group_paths
        self.app_name = app_name
        self.prefix = prefix
        self.filter_unhandled_paths = filter_unhandled_paths
        self.kwargs = {}
        if buckets is not None:
            self.kwargs["buckets"] = buckets
        self.skip_paths = []
        if skip_paths is not None:
            self.skip_paths = skip_paths
        self.optional_metrics_list = []
        if optional_metrics is not None:
            self.optional_metrics_list = optional_metrics
        self.always_use_int_status = always_use_int_status

        self.labels = OrderedDict(labels) if labels is not None else None

    # Starlette initialises middleware multiple times, so store metrics on the class
    @property
    def request_count(self):
        metric_name = f"{self.prefix}_requests_total"
        if metric_name not in PrometheusMiddleware._metrics:
            PrometheusMiddleware._metrics[metric_name] = Counter(
                metric_name,
                "Total HTTP requests",
                (
                    "method",
                    "path",
                    "status_code",
                    "app_name",
                    *self._default_label_keys(),
                ),
            )
        return PrometheusMiddleware._metrics[metric_name]

    @property
    def response_body_size_count(self):
        """
        Optional metric for tracking the size of response bodies.
        If using gzip middleware, you should test that the starlette_exporter middleware computes
        the proper response size value. Please post any feedback on this metric as an issue
        at https://github.com/stephenhillier/starlette_exporter.

        """
        if (
            self.optional_metrics_list != None
            and optional_metrics.response_body_size in self.optional_metrics_list
        ):
            metric_name = f"{self.prefix}_response_body_bytes_total"
            if metric_name not in PrometheusMiddleware._metrics:
                PrometheusMiddleware._metrics[metric_name] = Counter(
                    metric_name,
                    "Total HTTP response body bytes",
                    (
                        "method",
                        "path",
                        "status_code",
                        "app_name",
                        *self._default_label_keys(),
                    ),
                )
            return PrometheusMiddleware._metrics[metric_name]
        else:
            pass

    @property
    def request_body_size_count(self):
        """
        Optional metric tracking the received content-lengths of request bodies
        """
        if (
            self.optional_metrics_list != None
            and optional_metrics.request_body_size in self.optional_metrics_list
        ):
            metric_name = f"{self.prefix}_request_body_bytes_total"
            if metric_name not in PrometheusMiddleware._metrics:
                PrometheusMiddleware._metrics[metric_name] = Counter(
                    metric_name,
                    "Total HTTP request body bytes",
                    (
                        "method",
                        "path",
                        "status_code",
                        "app_name",
                        *self._default_label_keys(),
                    ),
                )
            return PrometheusMiddleware._metrics[metric_name]
        else:
            pass

    @property
    def request_time(self):
        metric_name = f"{self.prefix}_request_duration_seconds"
        if metric_name not in PrometheusMiddleware._metrics:
            PrometheusMiddleware._metrics[metric_name] = Histogram(
                metric_name,
                "HTTP request duration, in seconds",
                (
                    "method",
                    "path",
                    "status_code",
                    "app_name",
                    *self._default_label_keys(),
                ),
                **self.kwargs,
            )
        return PrometheusMiddleware._metrics[metric_name]

    @property
    def requests_in_progress(self):
        metric_name = f"{self.prefix}_requests_in_progress"
        if metric_name not in PrometheusMiddleware._metrics:
            PrometheusMiddleware._metrics[metric_name] = Gauge(
                metric_name,
                "Total HTTP requests currently in progress",
                ("method", "app_name", *self._default_label_keys()),
                multiprocess_mode="livesum",
            )
        return PrometheusMiddleware._metrics[metric_name]

    def _default_label_keys(self) -> List[str]:
        if self.labels is None:
            return []
        return list(self.labels.keys())

    def _default_label_values(self, request: Request):
        if self.labels is None:
            return []

        values: List[str] = []

        for k, v in self.labels.items():
            if isinstance(v, Callable):
                parsed_value = ""
                # if provided a callable, try to use it on the request.
                try:
                    result = v(request)
                except Exception:
                    logger.warn(f"label function for {k} failed", exc_info=True)
                else:
                    parsed_value = str(result)
                values.append(parsed_value)
                continue

            values.append(v)

        return values

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ["http"]:
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)

        method = request.method
        path = request.url.path

        if path in self.skip_paths:
            await self.app(scope, receive, send)
            return

        begin = time.perf_counter()
        end = None

        default_labels = self._default_label_values(request)

        # Increment requests_in_progress gauge when request comes in
        self.requests_in_progress.labels(method, self.app_name, *default_labels).inc()

        # Default status code used when the application does not return a valid response
        # or an unhandled exception occurs.
        status_code = 500

        # optional request and response body size metrics
        response_body_size: int = 0

        request_body_size: int = 0
        if (
            self.optional_metrics_list != None
            and optional_metrics.request_body_size in self.optional_metrics_list
        ):
            if request.headers.get("content-length"):
                request_body_size = int(request.headers["content-length"])

        async def wrapped_send(message: Message) -> None:
            if message["type"] == "http.response.start":
                nonlocal status_code
                status_code = message["status"]

                if self.always_use_int_status:
                    try:
                        status_code = int(message["status"])
                    except ValueError as e:
                        logger.warning(
                            f"always_use_int_status flag selected but failed to convert status_code to int for value: {status_code}"
                        )

                # find response body size for optional metric
                if (
                    self.optional_metrics_list != None
                    and optional_metrics.response_body_size
                    in self.optional_metrics_list
                ):
                    nonlocal response_body_size
                    for message_content_length in message["headers"]:
                        if (
                            message_content_length[0].decode("utf-8")
                            == "content-length"
                        ):
                            response_body_size += int(
                                message_content_length[1].decode("utf-8")
                            )

            if message["type"] == "http.response.body":
                nonlocal end
                end = time.perf_counter()

            await send(message)

        try:
            await self.app(scope, receive, wrapped_send)
        finally:
            # Decrement 'requests_in_progress' gauge after response sent
            self.requests_in_progress.labels(
                method, self.app_name, *default_labels
            ).dec()

            if self.filter_unhandled_paths or self.group_paths:
                grouped_path = self._get_router_path(scope)

                # filter_unhandled_paths removes any requests without mapped endpoint from the metrics.
                if self.filter_unhandled_paths and grouped_path is None:
                    return

                # group_paths enables returning the original router path (with url param names)
                # for example, when using this option, requests to /api/product/1 and /api/product/3
                # will both be grouped under /api/product/{product_id}. See the README for more info.
                if self.group_paths and grouped_path is not None:
                    path = grouped_path

            labels = [method, path, status_code, self.app_name, *default_labels]

            # optional response body size metric
            if (
                self.optional_metrics_list != None
                and optional_metrics.response_body_size in self.optional_metrics_list
            ):
                self.response_body_size_count.labels(*labels).inc(response_body_size)

            # optional request body size metric
            if (
                self.optional_metrics_list != None
                and optional_metrics.request_body_size in self.optional_metrics_list
            ):
                self.request_body_size_count.labels(*labels).inc(request_body_size)

            # if we were not able to set end when the response body was written,
            # set it now.
            if end is None:
                end = time.perf_counter()

            self.request_count.labels(*labels).inc()
            self.request_time.labels(*labels).observe(end - begin)

    @staticmethod
    def _get_router_path(scope: Scope) -> Optional[str]:
        """Returns the original router path (with url param names) for given request."""
        if not (scope.get("endpoint", None) and scope.get("router", None)):
            return None

        root_path = scope.get("root_path", "")
        app = scope.get("app", {})

        if hasattr(app, "root_path"):
            app_root_path = getattr(app, "root_path")
            if root_path.startswith(app_root_path):
                root_path = root_path[len(app_root_path) :]

        base_scope = {
            "type": scope.get("type"),
            "path": root_path + scope.get("path"),
            "path_params": scope.get("path_params", {}),
            "method": scope.get("method"),
        }

        try:
            path = get_matching_route_path(base_scope, scope.get("router").routes)
            return path
        except:
            # unhandled path
            pass

        return None
