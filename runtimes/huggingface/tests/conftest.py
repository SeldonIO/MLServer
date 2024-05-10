import pytest
import asyncio

from mlserver.utils import install_uvloop_event_loop


# test a prediction spend long time, so add this command argument to enable test tasks
# if not provide this command argument, task tests skiped
def pytest_addoption(parser):
    parser.addoption("--test-hg-tasks", action="store_true", default=False)


@pytest.fixture()
def event_loop():
    # NOTE: We need to override the `event_loop` fixture to change its scope to
    # `module`, so that it can be used downstream on other `module`-scoped
    # fixtures
    install_uvloop_event_loop()
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
