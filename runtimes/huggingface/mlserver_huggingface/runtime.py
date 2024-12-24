import asyncio
import torch

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

from prometheus_client import (
    Counter,
)


class HuggingFaceRuntime(MLModel):
    """Runtime class for specific Huggingface models"""

    def __init__(self, settings: ModelSettings):
        self.hf_settings = get_huggingface_settings(settings)
        super().__init__(settings)

        self._ModelInputTokens = Counter(
            "model_input_tokens",
            "Model input tokens count",
            ["model", "version"],
        )

        self._ModelOutputTokens = Counter(
            "model_output_tokens",
            "Model output tokens count",
            ["model", "version"],
        )

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

        #  calculate input_tokens
        if hasattr(self._model, "tokenizer") and args:
            input_texts = args[0] if isinstance(args[0], list) else [args[0]]
            input_tokens_count = sum(
                len(self._model.tokenizer(text, return_tensors="pt")["input_ids"][0]) for text in input_texts
            )
        else:
            input_tokens_count = 0

        prediction = self._model(*args, **kwargs)

        try:
            # calculate output_tokens
            if hasattr(self._model, "tokenizer") and prediction:
                output_tokens_count = sum(
                    len(self._model.tokenizer(text["generated_text"], return_tensors="pt")["input_ids"][0]) for text in prediction
                )
            else:
                output_tokens_count = 0

            # store metrics
            labels = dict(model=self.name, version=self.version)
            self._ModelInputTokens.labels(**labels).inc(input_tokens_count)
            self._ModelOutputTokens.labels(**labels).inc(output_tokens_count)
        except Exception as e:
            logger.error(f"got error: '{e}'")

        return self.encode_response(
            payload=prediction, default_codec=HuggingfaceRequestCodec
        )

    async def unload(self) -> bool:
        # TODO: Free up Tensorflow's GPU memory
        is_torch = self._model.framework == "pt"
        if not is_torch:
            return True

        uses_gpu = torch.cuda.is_available() and self._model.device != -1
        if not uses_gpu:
            # Nothing to free
            return True

        # Free up Torch's GPU memory
        torch.cuda.empty_cache()
        return True

    def _merge_metadata(self) -> None:
        meta = METADATA.get(self.hf_settings.task)
        if meta:
            self.inputs += meta.get("inputs", [])  # type: ignore
            self.outputs += meta.get("outputs", [])  # type: ignore
