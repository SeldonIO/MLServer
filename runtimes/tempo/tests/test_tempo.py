import pytest
import os

from tempo.serve.pipeline import Pipeline
from mlserver.types import InferenceRequest
from mlserver.utils import to_ndarray
from mlserver.settings import ModelSettings

from mlserver_tempo import TempoModel
from mlserver_tempo.tempo import WELLKNOWN_MODEL_FILENAMES


def test_load(model: TempoModel):
    assert model.ready
    assert isinstance(model._pipeline, Pipeline)


@pytest.mark.parametrize("fname", WELLKNOWN_MODEL_FILENAMES)
async def test_load_folder(fname, pipeline_uri: str, model_settings: ModelSettings):
    model_folder = os.path.dirname(pipeline_uri)
    model_path = os.path.join(model_folder, fname)
    os.rename(pipeline_uri, model_path)

    model_settings.parameters.uri = model_path  # type: ignore

    model = TempoModel(model_settings)
    await model.load()

    assert model.ready
    assert isinstance(model._pipeline, Pipeline)


async def test_predict(
    model: TempoModel, inference_request: InferenceRequest, inference_pipeline: Pipeline
):
    res = await model.predict(inference_request)

    assert len(res.outputs) == 1

    pipeline_input = to_ndarray(inference_request.inputs[0])
    expected_output = inference_pipeline(pipeline_input)

    pipeline_output = res.outputs[0].data

    assert expected_output.tolist() == pipeline_output
