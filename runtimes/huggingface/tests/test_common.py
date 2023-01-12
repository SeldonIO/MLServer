import pytest
from typing import Dict
from mlserver_huggingface.common import HuggingFaceSettings


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
