import asyncio
import torch
from typing import Any
from mlserver.model import MLModel
from mlserver.settings import ModelSettings
from mlserver.logging import logger
from mlserver.types import (
    InferenceRequest,
    InferenceResponse,
)

from .settings import get_huggingface_settings
from .common import load_pipeline_from_settings
from .codecs import HuggingfaceRequestCodec, ChariotImgModelOutputCodec
from .metadata import METADATA

CHARIOT_IMAGE_TASK = [
    "image-classification",
    "image-segmentation",
    "object-detection",
]


class HuggingFaceRuntime(MLModel):
    """Runtime class for specific Huggingface models"""

    def __init__(self, settings: ModelSettings):
        self.hf_settings = get_huggingface_settings(settings)
        super().__init__(settings)

    async def load(self) -> bool:
        logger.info(f"Loading model for task '{self.hf_settings.task_name}'...")
        loop = asyncio.get_running_loop()
        [self._model] = await asyncio.gather(
            loop.run_in_executor(
                None,
                load_pipeline_from_settings,
                self.hf_settings,
                self.settings,
            )
        )
        self._merge_metadata()
        return True

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        # TODO: convert and validate?
        kwargs = HuggingfaceRequestCodec.decode_request(payload)
        args = kwargs.pop("args", [])
        array_inputs = kwargs.pop("array_inputs", [])
        if array_inputs:
            args = [list(array_inputs)] + args
        predict_proba, predict_proba_kwargs = self.get_predict_proba_kwargs(payload)
        predictions = self._model(*args, **kwargs, **predict_proba_kwargs)
        if self.hf_settings.task in CHARIOT_IMAGE_TASK:
            predictions = ChariotImgModelOutputCodec.encode_output(
                predictions,
                task_type=self.hf_settings.task,
                class_int_to_str=self._model.model.config.id2label,
                predict_proba=predict_proba,
            )
        response = self.encode_response(
            payload=predictions, default_codec=HuggingfaceRequestCodec
        )
        return response

    def get_predict_proba_kwargs(
        self, payload: InferenceRequest
    ) -> tuple[bool, dict[str, Any]]:
        actions = {
            (
                getattr(request_input.parameters, "action", "predict")
                if request_input.parameters
                else "predict"
            )
            for request_input in payload.inputs
        }
        if len(actions) > 1:
            raise ValueError(
                f"If processing a batch all 'actions' must be the same \
                but got 'actions': {actions}"
            )
        action = actions.pop()
        predict_proba = action == "predict_proba"
        predict_proba_kwargs = dict()
        if predict_proba and self.hf_settings.task == "image-classification":
            predict_proba_kwargs["top_k"] = self._model.model.config.num_labels
        return predict_proba, predict_proba_kwargs

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
