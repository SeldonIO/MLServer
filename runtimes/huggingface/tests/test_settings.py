import pytest

from typing import Dict

from mlserver.settings import ModelSettings, ModelParameters

from mlserver_huggingface.runtime import HuggingFaceRuntime
from mlserver_huggingface.settings import (
    HuggingFaceSettings,
    ExtraDict,
    PARAMETERS_ENV_NAME,
    get_huggingface_settings,
    merge_huggingface_settings_extra,
)
from mlserver_huggingface.errors import MissingHuggingFaceSettings


@pytest.fixture()
def model_settings_extra_task():
    return ModelSettings(
        name="foo",
        implementation=HuggingFaceRuntime,
        parameters=ModelParameters(
            extra={"task": "text-generation", "pretrained_model": "distilgpt2"}
        ),
    )


@pytest.fixture()
def model_settings_extra_none():
    return ModelSettings(
        name="foo",
        implementation=HuggingFaceRuntime,
        parameters=ModelParameters(extra=None),
    )


@pytest.fixture()
def model_settings_extra_empty():
    return ModelSettings(
        name="foo",
        implementation=HuggingFaceRuntime,
        parameters=ModelParameters(extra={}),
    )


@pytest.mark.parametrize(
    "model_settings,env_params,expected",
    [
        (
            "model_settings_extra_task",
            {"task": "question-answering"},
            {"task": "question-answering", "pretrained_model": "distilgpt2"},
        ),
        (
            "model_settings_extra_task",
            {},
            {"task": "text-generation", "pretrained_model": "distilgpt2"},
        ),
        (
            "model_settings_extra_none",
            {"task": "question-answering"},
            {"task": "question-answering"},
        ),
        (
            "model_settings_extra_empty",
            {"task": "question-answering"},
            {"task": "question-answering"},
        ),
    ],
)
def test_merge_huggingface_settings_extra(
    model_settings: str,
    env_params: ExtraDict,
    expected: Dict,
    request: pytest.FixtureRequest,
):
    assert expected == merge_huggingface_settings_extra(
        request.getfixturevalue(model_settings), env_params
    )


def test_merge_huggingface_settings_extra_raises(model_settings_extra_none):
    with pytest.raises(MissingHuggingFaceSettings):
        merge_huggingface_settings_extra(model_settings_extra_none, {})


@pytest.mark.parametrize(
    "model_settings,env_params,expected",
    [
        (
            "model_settings_extra_task",
            '[{"name": "task", "value": "question-answering", "type": "STRING"}]',
            HuggingFaceSettings(
                task="question-answering",
                task_suffix="",
                pretrained_model="distilgpt2",
                pretrained_tokenizer=None,
                framework=None,
                optimum_model=False,
                device=None,
                inter_op_threads=None,
                intra_op_threads=None,
            ),
        ),
        (
            "model_settings_extra_task",
            "[]",
            HuggingFaceSettings(
                task="text-generation",
                task_suffix="",
                pretrained_model="distilgpt2",
                pretrained_tokenizer=None,
                framework=None,
                optimum_model=False,
                device=None,
                inter_op_threads=None,
                intra_op_threads=None,
            ),
        ),
        (
            "model_settings_extra_none",
            '[{"name": "task", "value": "question-answering", "type": "STRING"}]',
            HuggingFaceSettings(
                task="question-answering",
                task_suffix="",
                pretrained_model=None,
                pretrained_tokenizer=None,
                framework=None,
                optimum_model=False,
                device=None,
                inter_op_threads=None,
                intra_op_threads=None,
            ),
        ),
        (
            "model_settings_extra_empty",
            '[{"name": "task", "value": "question-answering", "type": "STRING"}]',
            HuggingFaceSettings(
                task="question-answering",
                task_suffix="",
                pretrained_model=None,
                pretrained_tokenizer=None,
                framework=None,
                optimum_model=False,
                device=None,
                inter_op_threads=None,
                intra_op_threads=None,
            ),
        ),
    ],
)
def test_get_huggingface_settings(
    model_settings: str,
    env_params: str,
    expected: HuggingFaceSettings,
    request: pytest.FixtureRequest,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setenv(PARAMETERS_ENV_NAME, env_params)

    assert expected == get_huggingface_settings(request.getfixturevalue(model_settings))

    monkeypatch.delenv(PARAMETERS_ENV_NAME)


def test_get_huggingface_settings_raises(model_settings_extra_none):
    with pytest.raises(MissingHuggingFaceSettings):
        get_huggingface_settings(model_settings_extra_none)


@pytest.mark.parametrize(
    "extra, expected_model_kwargs",
    [
        (
            {
                "task": "text-generation",
                "task_suffix": "_en",
                "pretrained_model": "gpt2"
            },
            {"torch_dtype": "auto"}
        ),
        (
            {
                "task": "text-generation",
                "task_suffix": "_en",
                "pretrained_model": "gpt2",
                "model_kwargs": {"some_other_key": "value","torch_dtype": "float32"}
            },
            {"some_other_key": "value","torch_dtype": "float32"}
        ),
        (
            {
                "task": "text-generation",
                "task_suffix": "_en",
                "pretrained_model": "gpt2",
                "model_kwargs": {"some_other_key": "value"}
            },
            {"some_other_key": "value","torch_dtype": "auto"}
        )
    ]
)
def test_huggingface_settings(extra, expected_model_kwargs):
    hf_settings = HuggingFaceSettings(**extra)
    assert hf_settings.task == extra.get("task", "")
    assert hf_settings.task_suffix == extra.get("task_suffix", "")
    assert hf_settings.pretrained_model == extra.get("pretrained_model", None)
    assert hf_settings.model_kwargs == expected_model_kwargs