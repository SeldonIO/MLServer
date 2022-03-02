import pytest
from mlserver.settings import ModelSettings
from mlserver.codecs import CodecError
from mlserver.types import RequestInput, InferenceRequest
from mlserver_alibi_detect import AlibiDetectRuntime
from alibi_detect.cd import TabularDrift


def test_load(model: AlibiDetectRuntime):
    assert model.ready
    assert type(model._model) == TabularDrift


async def test_load_folder(model_uri: str, model_settings: ModelSettings):

    model_settings.parameters.uri = model_uri  # type: ignore

    model = AlibiDetectRuntime(model_settings)
    await model.load()

    assert model.ready
    assert type(model._model) == TabularDrift


async def test_predict(model: AlibiDetectRuntime, inference_request: InferenceRequest):
    response = await model.predict(inference_request)

    assert len(response.outputs) == 4
    assert 0 <= response.outputs[0].data[0] <= 1


async def test_multiple_inputs_error(
    model: AlibiDetectRuntime, inference_request: InferenceRequest
):
    inference_request.inputs.append(
        RequestInput(name="input-1", shape=[1, 2], data=[[0, 1]], datatype="FP32")
    )

    with pytest.raises(CodecError):
        await model.predict(inference_request)
