from mlserver.settings import ModelSettings, ModelParameters
from mlserver_huggingface import HuggingFaceRuntime


def case_optimum_settings() -> ModelSettings:
    return ModelSettings(
        name="foo",
        implementation=HuggingFaceRuntime,
        parameters=ModelParameters(
            extra={
                "task": "text-generation",
                "pretrained_model": "distilgpt2",
                "optimum_model": True,
            }
        ),
    )


def case_transformers_settings() -> ModelSettings:
    return ModelSettings(
        name="foo",
        implementation=HuggingFaceRuntime,
        parameters=ModelParameters(
            extra={
                "task": "question-answering",
                "optimum_model": False,
            }
        ),
    )
