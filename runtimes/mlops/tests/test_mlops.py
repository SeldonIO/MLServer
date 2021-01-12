import inspect
import pytest

from mlserver.types import InferenceRequest, RequestInput
from mlserver.errors import InferenceError
from mlserver.utils import to_ndarray

from mlserver_mlops import MLOpsModel

from .conftest import SumPipeline


def test_load(model: MLOpsModel):
    assert model.ready
    assert hasattr(model._pipeline, "pipeline")
    assert inspect.ismethod(model._pipeline.pipeline)


async def test_multiple_inputs_error(
    model: MLOpsModel, inference_request: InferenceRequest
):
    inference_request.inputs.append(
        RequestInput(name="input-1", shape=[2], data=[0, 1], datatype="FP32")
    )

    with pytest.raises(InferenceError):
        await model.predict(inference_request)


async def test_predict(
    model: MLOpsModel, inference_request: InferenceRequest, pipeline: SumPipeline
):
    res = await model.predict(inference_request)

    assert len(res.outputs) == 1

    pipeline_input = to_ndarray(inference_request.inputs[0])
    expected_output = pipeline.pipeline(pipeline_input)

    pipeline_output = res.outputs[0].data

    assert expected_output.tolist() == pipeline_output
