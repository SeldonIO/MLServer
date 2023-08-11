from unittest.mock import MagicMock, patch

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
    "has_model_params, param_uri_value, expected",
    [
        (True, "", "./some-pretrained-folder"),
        (True, None, "./some-pretrained-folder"),
        (True, "/some/folder/model-artefacts", "./some-pretrained-folder"),
        (False, "", "./some-pretrained-folder"),
    ],
)
@patch("mlserver_huggingface.common._get_pipeline_class")
def test_pipeline_was_initialised_and_pretrained_model_takes_precedence(
    mock_pipeline_factory,
    has_model_params: bool,
    param_uri_value: Optional[str],
    expected: str,
):
    mock_pipeline_factory.return_value = MagicMock()

    hf_settings = HuggingFaceSettings(pretrained_model="./some-pretrained-folder")
    model_params = None
    if has_model_params:
        model_params = ModelParameters(uri=param_uri_value)

    model_settings = ModelSettings(
        name="foo",
        implementation=HuggingFaceRuntime,
        parameters=model_params,
    )

    _ = load_pipeline_from_settings(hf_settings, model_settings)

    mock_pipeline_factory.return_value.assert_called_once()
    pipeline_call_args = mock_pipeline_factory.return_value.call_args

    assert pipeline_call_args.kwargs["model"] == expected


@pytest.mark.parametrize(
    "empty_pretrained_model_value, has_model_params, param_uri_value, expected",
    [
        (None, True, None, None),
        (None, True, "", ""),
        (None, True, "/some/folder/model-artefacts", "/some/folder/model-artefacts"),
        (None, False, "", None),
        ("", True, None, None),
        ("", True, "", ""),
        ("", True, "/some/folder/model-artefacts", "/some/folder/model-artefacts"),
        ("", False, "", ""),
    ],
)
@patch("mlserver_huggingface.common._get_pipeline_class")
def test_pipeline_was_initialised_when_pretrained_model_is_not_supplied(
    mock_pipeline_factory,
    empty_pretrained_model_value: Optional[str],
    has_model_params: bool,
    param_uri_value: Optional[str],
    expected: str,
):
    mock_pipeline_factory.return_value = MagicMock()

    hf_settings = HuggingFaceSettings(pretrained_model=empty_pretrained_model_value)
    model_params = None
    if has_model_params:
        model_params = ModelParameters(uri=param_uri_value)

    model_settings = ModelSettings(
        name="foo",
        implementation=HuggingFaceRuntime,
        parameters=model_params,
    )

    _ = load_pipeline_from_settings(hf_settings, model_settings)

    mock_pipeline_factory.return_value.assert_called_once()
    pipeline_call_args = mock_pipeline_factory.return_value.call_args

    assert pipeline_call_args.kwargs["model"] == expected
