import pytest
import asyncio

from mlserver.utils import install_uvloop_event_loop
from mlserver.types import InferenceRequest, RequestInput
from mlserver.settings import ModelSettings, ModelParameters

from mlserver_huggingface import HuggingFaceRuntime


# test a prediction spend long time, so add this command argument to enable test tasks
# if not provide this command argument, task tests skiped
def pytest_addoption(parser):
    parser.addoption("--test-hg-tasks", action="store_true", default=False)


@pytest.fixture(scope="module")
def event_loop():
    # NOTE: We need to override the `event_loop` fixture to change its scope to
    # `module`, so that it can be used downstream on other `module`-scoped
    # fixtures
    install_uvloop_event_loop()
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
def model_settings() -> ModelSettings:
    return ModelSettings(
        name="foo",
        implementation=HuggingFaceRuntime,
        parameters=ModelParameters(
            extra={
                "task": "question-answering",
            }
        ),
    )


@pytest.fixture(scope="module")
async def runtime(model_settings: ModelSettings) -> HuggingFaceRuntime:
    runtime = HuggingFaceRuntime(model_settings)
    await runtime.load()
    return runtime


@pytest.fixture
def inference_request() -> InferenceRequest:
    return InferenceRequest(
        inputs=[
            RequestInput(
                name="question",
                shape=[1],
                datatype="BYTES",
                data=["what is your name?"],
            ),
            RequestInput(
                name="context",
                shape=[1],
                datatype="BYTES",
                data=["Hello, I am Seldon, how is it going"],
            ),
        ]
    )
