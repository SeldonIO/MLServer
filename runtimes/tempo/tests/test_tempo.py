import pytest

from tempo.serve.pipeline import Pipeline
from mlserver.types import InferenceRequest, RequestInput
from mlserver.errors import InferenceError
from mlserver.utils import to_ndarray

from mlserver_tempo import TempoModel


def test_load(model: TempoModel):
    assert model.ready
    assert isinstance(model._pipeline, Pipeline)


async def test_multiple_inputs_error(
    model: TempoModel, inference_request: InferenceRequest
):
    inference_request.inputs.append(
        RequestInput(name="input-1", shape=[2], data=[0, 1], datatype="FP32")
    )

    with pytest.raises(InferenceError):
        await model.predict(inference_request)


async def test_predict(
    model: TempoModel, inference_request: InferenceRequest, inference_pipeline: Pipeline
):
    res = await model.predict(inference_request)

    assert len(res.outputs) == 1

    pipeline_input = to_ndarray(inference_request.inputs[0])
    expected_output = inference_pipeline(pipeline_input)

    pipeline_output = res.outputs[0].data

    assert expected_output.tolist() == pipeline_output
