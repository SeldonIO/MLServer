import pytest
import asyncio


# test a prediction spend long time, so add this command argument to enable test tasks
# if not provide this command argument, task tests skiped
def pytest_addoption(parser):
    parser.addoption("--test-hg-tasks", action="store_true", default=False)
