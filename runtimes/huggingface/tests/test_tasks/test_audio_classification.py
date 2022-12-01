import pytest
from mlserver.types import InferenceRequest, RequestInput, Parameters
from mlserver.settings import ModelSettings, ModelParameters
from mlserver_huggingface import HuggingFaceRuntime


@pytest.fixture
def current_model_settings(request) -> ModelSettings:
    if not request.config.option.test_hg_tasks:
        pytest.skip()
    return ModelSettings(
        name="model",
        implementation=HuggingFaceRuntime,
        parameters=ModelParameters(
            extra={
                "task": "audio-classification",
            }
        ),
    )


@pytest.fixture
async def current_runtime(current_model_settings: ModelSettings) -> HuggingFaceRuntime:
    runtime = HuggingFaceRuntime(current_model_settings)
    await runtime.load()
    return runtime


@pytest.fixture
def filepath_input(audio_filepath):
    return InferenceRequest(
        inputs=[
            RequestInput(
                name="inputs",
                datatype="BYTES",
                shape=[1],
                data=[audio_filepath],
                parameters=Parameters(content_type="str"),
            )
        ]
    )


@pytest.fixture
def bytes_input(audio_filebytes):
    return InferenceRequest(
        inputs=[
            RequestInput(
                name="inputs",
                datatype="BYTES",
                shape=[1],
                data=[audio_filebytes],
                parameters=Parameters(content_type="base64"),
            )
        ]
    )


async def test_filepath_infer(current_runtime, filepath_input):
    resp = await current_runtime.predict(filepath_input)
    assert len(resp.outputs) == 1


async def test_bytes_infer(current_runtime, bytes_input):
    resp = await current_runtime.predict(bytes_input)
    assert len(resp.outputs) == 1
