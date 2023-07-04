import asyncio

from mlserver.model import MLModel
from mlserver.settings import ModelSettings
from mlserver.logging import logger
from mlserver.types import (
    InferenceRequest,
    InferenceResponse,
)

from .settings import get_huggingface_settings
from .common import load_pipeline_from_settings
from .codecs import HuggingfaceRequestCodec
from .metadata import METADATA


class HuggingFaceRuntime(MLModel):
    """Runtime class for specific Huggingface models"""

    def __init__(self, settings: ModelSettings):
        self.hf_settings = get_huggingface_settings(settings)
        super().__init__(settings)

    async def load(self) -> bool:
        # Loading & caching pipeline in asyncio loop to avoid blocking
        logger.info(f"Loading model for task '{self.hf_settings.task_name}'...")
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
        kwargs = HuggingfaceRequestCodec.decode_request(payload)
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
