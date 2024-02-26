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
    "pretrained_model, parameters_uri, expected",
    [
        (None, None, None),
        (None, "", ""),
        (None, "/some/folder/model-artefacts", "/some/folder/model-artefacts"),
        ("", None, None),
        ("", "", ""),
        ("", "/some/folder/model-artefacts", "/some/folder/model-artefacts"),
        ("some-model", None, "some-model"),
        ("some-model", "", "some-model"),
        ("some-model", "/some/folder/model-artefacts", "some-model"),
        (
            "/some/other/folder/model-artefacts",
            None,
            "/some/other/folder/model-artefacts",
        ),
        (
            "/some/other/folder/model-artefacts",
            "",
            "/some/other/folder/model-artefacts",
        ),
        (
            "/some/other/folder/model-artefacts",
            "/some/folder/model-artefacts",
            "/some/other/folder/model-artefacts",
        ),
    ],
)
@patch("mlserver_huggingface.common._get_pipeline_class")
def test_pipeline_is_initialised_with_correct_model_param(
    mock_pipeline_factory,
    pretrained_model: Optional[str],
    parameters_uri: Optional[str],
    expected: Optional[str],
):
    mock_pipeline_factory.return_value = MagicMock()

    hf_settings = HuggingFaceSettings(pretrained_model=pretrained_model)
    model_params = ModelParameters(uri=parameters_uri)

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
    "pretrained_model, task, input_batch_size, expected_batch_size",
    [
        (
            "hf-internal-testing/tiny-bert-for-token-classification",
            "token-classification",
            1,
            1,
        ),
        (
            "hf-internal-testing/tiny-bert-for-token-classification",
            "token-classification",
            0,
            1,
        ),
        (
            "hf-internal-testing/tiny-bert-for-token-classification",
            "token-classification",
            10,
            1,
        ),  # Neither pad_token nor eos_token defined revert to 1
    ],
)
def test_pipeline_checks_for_eos_and_pad_token(
    pretrained_model: str,
    task: Optional[str],
    input_batch_size: Optional[int],
    expected_batch_size: Optional[int],
):
    hf_settings = HuggingFaceSettings(pretrained_model=pretrained_model, task=task)
    model_params = ModelParameters()
    model_settings = ModelSettings(
        name="foo",
        implementation=HuggingFaceRuntime,
        parameters=model_params,
        max_batch_size=input_batch_size,
    )

    m = load_pipeline_from_settings(hf_settings, model_settings)

    assert m._batch_size == expected_batch_size
