import numpy as np

from pydantic.error_wrappers import ValidationError
from typing import Optional, List
from pydantic import BaseSettings
from functools import cached_property

from alibi_detect.saving import load_detector

from mlserver.batching import BatchedRequests
from mlserver.types import InferenceRequest, InferenceResponse
from mlserver.settings import ModelSettings
from mlserver.model import MLModel
from mlserver.codecs import NumpyCodec, NumpyRequestCodec
from mlserver.utils import get_model_uri
from mlserver.errors import MLServerError, InferenceError

ENV_PREFIX_ALIBI_DETECT_SETTINGS = "MLSERVER_MODEL_ALIBI_DETECT_"

ALIBI_MODULE_NAMES = {"cd": "drift", "od": "outlier", "ad": "adversarial"}


class AlibiDetectSettings(BaseSettings):
    """
    Parameters that apply only to alibi detect models
    """

    class Config:
        env_prefix = ENV_PREFIX_ALIBI_DETECT_SETTINGS

    predict_parameters: dict = {}
    """
    Keyword parameters to pass to the detector's `predict` method.
    """

    batch_size: Optional[int] = None
    """
    Run the detector after accumulating a batch of size `batch_size`.
    Note that this is different to MLServer's adaptive batching, since the rest
    of requests will just return empty (i.e. instead of being hold until
    inference runs for all of them).
    """


class AlibiDetectRuntime(MLModel):
    """
    Implementation of the MLModel interface to load and serve `alibi-detect` models.
    """

    def __init__(self, settings: ModelSettings):
        if settings.parameters is None:
            self._ad_settings = AlibiDetectSettings()
        else:
            extra = settings.parameters.extra
            self._ad_settings = AlibiDetectSettings(**extra)  # type: ignore

        self._batch: List[InferenceRequest] = []
        super().__init__(settings)

    async def load(self) -> bool:
        model_uri = await get_model_uri(self._settings)
        try:
            self._model = load_detector(model_uri)
        except (
            ValueError,
            FileNotFoundError,
            EOFError,
            NotImplementedError,
            ValidationError,
        ) as e:
            raise MLServerError(
                f"Invalid configuration for model {self._settings.name}: {e}"
            ) from e

        return True

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        # If batch is not configured, run the detector and return the output
        if not self._ad_settings.batch_size:
            return self._detect(payload)

        if len(self._batch) < self._ad_settings.batch_size:
            self._batch.append(payload)

        if len(self._batch) >= self._ad_settings.batch_size:
            batched = self._get_batched_request()
            return self._detect(batched)

        return InferenceResponse(
            model_name=self.name, model_version=self.version, outputs=[]
        )

    def _get_batched_request(self) -> InferenceRequest:
        # Build requests dictionary with mocked IDs.
        # This is required by the BatchedRequests util.
        inference_requests = {}
        for idx, inference_request in enumerate(self._batch):
            inference_requests[str(idx)] = inference_request

        batched = BatchedRequests(inference_requests)
        self._batch = []
        return batched.merged_request

    def _detect(self, payload: InferenceRequest) -> InferenceResponse:
        input_data = self.decode_request(payload, default_codec=NumpyRequestCodec)
        predict_kwargs = self._ad_settings.predict_parameters

        try:
            y = self._model.predict(np.array(input_data), **predict_kwargs)
            return self._encode_response(y)
        except (ValueError, IndexError) as e:
            raise InferenceError(
                f"Invalid predict parameters for model {self._settings.name}: {e}"
            ) from e

    def _encode_response(self, y: dict) -> InferenceResponse:
        outputs = []
        for key in y["data"]:
            outputs.append(
                NumpyCodec.encode_output(name=key, payload=np.array([y["data"][key]]))
            )

        # Add headers
        y["meta"]["headers"] = {
            "x-seldon-alibi-type": self.alibi_type,
            "x-seldon-alibi-method": self.alibi_method,
        }
        return InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            parameters=y["meta"],
            outputs=outputs,
        )

    @cached_property
    def alibi_method(self) -> str:
        module: str = type(self._model).__module__
        return module.split(".")[-1]

    @cached_property
    def alibi_type(self) -> str:
        module: str = type(self._model).__module__
        method = module.split(".")[-2]
        if method in ALIBI_MODULE_NAMES:
            return ALIBI_MODULE_NAMES[method]
        else:
            return "unknown"
