from mlserver.rest.server import RESTServer
from mlserver.rest.utils import to_scope

from ..fixtures import SumModel

from ..metrics.conftest import prometheus_registry
from prometheus_client.registry import CollectorRegistry


def test_add_custom_handlers(
    prometheus_registry: CollectorRegistry, rest_server: RESTServer, sum_model: SumModel
):
    scope = to_scope(sum_model.my_payload.__custom_handler__)
    found_route = None
    for route in rest_server._app.routes:
        match, _ = route.matches(scope)
        if match == match.FULL:
            found_route = route
            break

    assert found_route is not None


async def test_delete_custom_handlers(
    prometheus_registry: CollectorRegistry, rest_server: RESTServer, sum_model: SumModel
):
    await rest_server.delete_custom_handlers(sum_model)

    scope = to_scope(sum_model.my_payload.__custom_handler__)
    for route in rest_server._app.routes:
        match, _ = route.matches(scope)
        assert match == match.NONE
