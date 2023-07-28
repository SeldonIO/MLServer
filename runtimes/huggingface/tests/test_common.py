from unittest.mock import patch, MagicMock

import pytest

from typing import Dict, Optional
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


@pytest.mark.parametrize(
    "hf_pretrained_model, has_model_params, uri_value, expected",
    [
        (None, True, None, None),
        (None, True, "", ""),
        (None, True, "/some/folder/model-artefacts", "/some/folder/model-artefacts"),
        (None, False, "N/A", None),
        ("", True, None, None),
        ("", True, "", ""),
        ("", True, "/some/folder/model-artefacts", "/some/folder/model-artefacts"),
        ("", False, "N/A", ""),
        ("./some-pretrained-folder", "N/A", "N/A", "./some-pretrained-folder"),
    ],
)
@patch("mlserver_huggingface.common._get_pipeline_class")
def test_pipeline_was_initialised_with_correct_model(
    mock_pipeline_factory,
    hf_pretrained_model: Optional[str],
    has_model_params: Optional[bool],
    uri_value: Optional[str],
    expected: Optional[str],
):
    mock_pipeline_factory.return_value = MagicMock()

    hf_settings = HuggingFaceSettings(pretrained_model=hf_pretrained_model)

    model_params = None
    if has_model_params:
        model_params = ModelParameters(uri=uri_value)

    model_settings = ModelSettings(
        name="foo",
        implementation=HuggingFaceRuntime,
        parameters=model_params,
    )

    _ = load_pipeline_from_settings(hf_settings, model_settings)

    mock_pipeline_factory.return_value.assert_called_once()

    pipeline_call_args = mock_pipeline_factory.return_value.call_args

    assert pipeline_call_args.kwargs["model"] == expected
