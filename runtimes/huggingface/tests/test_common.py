import pytest

from typing import Dict
from optimum.onnxruntime.modeling_ort import ORTModelForQuestionAnswering
from transformers.models.distilbert.modeling_distilbert import (
    DistilBertForQuestionAnswering,
)

from mlserver.settings import ModelSettings, ModelParameters

from mlserver_huggingface.runtime import HuggingFaceRuntime
from mlserver_huggingface.settings import HuggingFaceSettings
from mlserver_huggingface.common import load_pipeline_from_settings


@pytest.mark.parametrize(
    "envs, expected",
    [
        ({"task": "translation", "task_suffix": "_en_to_fr"}, "translation_en_to_fr"),
        (
            {"task": "question-answering", "task_suffix": "_any_thing_else"},
            "question-answering",
        ),
    ],
)
def test_settings_task_name(envs: Dict[str, str], expected: str):
    setting = HuggingFaceSettings(**envs)
    assert setting.task_name == expected


@pytest.mark.parametrize(
    "optimum_model, expected",
    [(True, ORTModelForQuestionAnswering), (False, DistilBertForQuestionAnswering)],
)
def test_load_pipeline(optimum_model: bool, expected):
    hf_settings = HuggingFaceSettings(
        task="question-answering", optimum_model=optimum_model
    )
    model_settings = ModelSettings(
        name="foo",
        implementation=HuggingFaceRuntime,
        parameters=ModelParameters(extra=hf_settings.dict()),
    )

    pipeline = load_pipeline_from_settings(hf_settings, model_settings)

    assert isinstance(pipeline.model, expected)
