import asyncio
from mlserver.model import MLModel
from mlserver.settings import ModelSettings
from mlserver.types import (
    InferenceRequest,
    InferenceResponse,
)
from transformers.pipelines import SUPPORTED_TASKS

from mlserver.logging import logger

from .errors import (
    MissingHuggingFaceSettings,
    InvalidHugginFaceTask,
    InvalidOptimumTask,
)
from .common import (
    HuggingFaceSettings,
    parse_parameters_from_env,
    load_pipeline_from_settings,
    SUPPORTED_OPTIMUM_TASKS,
)
from .codecs import HuggingfaceRequestCodec
from .metadata import METADATA


class HuggingFaceRuntime(MLModel):
    """Runtime class for specific Huggingface models"""

    def __init__(self, settings: ModelSettings):
        env_params = parse_parameters_from_env()
        if not env_params and (
            not settings.parameters or not settings.parameters.extra
        ):
            raise MissingHuggingFaceSettings()

        extra = env_params or settings.parameters.extra  # type: ignore
        self.hf_settings = HuggingFaceSettings(**extra)  # type: ignore

        if self.hf_settings.task not in SUPPORTED_TASKS:
            raise InvalidHugginFaceTask(self.hf_settings.task)

        if self.hf_settings.optimum_model:
            if self.hf_settings.task not in SUPPORTED_OPTIMUM_TASKS:
                raise InvalidOptimumTask(self.hf_settings.task)

        super().__init__(settings)

    async def load(self) -> bool:
        # Loading & caching pipeline in asyncio loop to avoid blocking
        logger.info("Loading model for task '{self.hf_settings.task_name}'...")
        await asyncio.get_running_loop().run_in_executor(
            None,
            load_pipeline_from_settings,
            self.hf_settings,
            self.settings,
        )

        # Now we load the cached model which should not block asyncio
        self._model = load_pipeline_from_settings(self.hf_settings, self.settings)
        self._merge_metadata()
        return True

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        # TODO: convert and validate?
        kwargs = self.decode_request(payload, default_codec=HuggingfaceRequestCodec)
        args = kwargs.pop("args", [])

        array_inputs = kwargs.pop("array_inputs", [])
        if array_inputs:
            args = [list(array_inputs)] + args
        prediction = self._model(*args, **kwargs)

        return self.encode_response(
            payload=prediction, default_codec=HuggingfaceRequestCodec
        )

    def _merge_metadata(self) -> None:
        meta = METADATA.get(self.hf_settings.task)
        if meta:
            self.inputs += meta.get("inputs", [])  # type: ignore
            self.outputs += meta.get("outputs", [])  # type: ignore
