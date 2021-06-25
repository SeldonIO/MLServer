from mlserver.rest.server import RESTServer

from ..fixtures import SumModel


def test_add_custom_handlers(rest_server: RESTServer, sum_model: SumModel):
    scope = {"type": "http", "method": "POST", "path": "/my-custom-endpoint"}
    found_route = None
    for route in rest_server._app.routes:
        match, _ = route.matches(scope)
        if match == match.FULL:
            found_route = route
            break

    assert found_route is not None
