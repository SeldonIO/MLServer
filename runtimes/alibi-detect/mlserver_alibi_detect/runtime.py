import os
import numpy as np

from pydantic import ValidationError
from typing import Optional, List, Dict
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import cached_property

from alibi_detect.saving import load_detector

import mlserver
from mlserver.batching import BatchedRequests
from mlserver.types import InferenceRequest, InferenceResponse
from mlserver.settings import ModelSettings
from mlserver.model import MLModel
from mlserver.codecs import NumpyCodec, NumpyRequestCodec
from mlserver.utils import get_model_uri
from mlserver.errors import MLServerError, InferenceError
from mlserver.logging import logger

ENV_PREFIX_ALIBI_DETECT_SETTINGS = "MLSERVER_MODEL_ALIBI_DETECT_"

ALIBI_MODULE_NAMES = {"cd": "drift", "od": "outlier", "ad": "adversarial"}


class AlibiDetectSettings(BaseSettings):
    """
    Parameters that apply only to alibi detect models
    """

    model_config = SettingsConfigDict(
        env_prefix=ENV_PREFIX_ALIBI_DETECT_SETTINGS,
    )

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

    state_save_freq: Optional[int] = Field(100, gt=0)
    """
    Save the detector state after every `state_save_freq` predictions.
    Only applicable to detectors with a `save_state` method.
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
        self._model_uri = await get_model_uri(self._settings)
        try:
            self._model = load_detector(self._model_uri)
            mlserver.register("seldon_model_drift", "Drift metrics")

            # Check whether an online drift detector (i.e. has a save_state method)
            self._online = True if hasattr(self._model, "save_state") else False
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
        if self._online or not self._ad_settings.batch_size:
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

        # If batch is configured or X has length 1, wrap X in a list to avoid unpacking
        X = np.array(input_data)
        if not self._online or len(input_data) == 1:
            X = [X]  # type: ignore[assignment]

        # Run detector inference
        pred = []
        for x in X:
            # Prediction
            try:
                current_pred = self._model.predict(x, **predict_kwargs)
                pred.append(current_pred)
                self._log_metrics(current_pred)
            except (ValueError, IndexError) as e:
                raise InferenceError(
                    f"Invalid predict parameters for model {self._settings.name}: {e}"
                ) from e
            # Save state if necessary
            if self._should_save_state:
                self._save_state()

        return self._encode_response(self._postproc_pred(pred))

    def _log_metrics(self, current_pred: dict) -> None:
        if "data" not in current_pred:
            return

        data = current_pred["data"]
        if "is_drift" in data:
            # NOTE: is_drift may be an array larger than 1 (e.g. if drift is
            # provided per input feature) or a single-value integer
            is_drift = data["is_drift"]
            if isinstance(is_drift, int):
                is_drift = [is_drift]

            for is_drift_instance in is_drift:
                mlserver.log(seldon_model_drift=is_drift_instance)

    def _encode_response(self, y: dict) -> InferenceResponse:
        outputs = []
        for key in y["data"]:
            outputs.append(
                NumpyCodec.encode_output(name=key, payload=np.array(y["data"][key]))
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

    @staticmethod
    def _postproc_pred(pred: List[dict]) -> dict:
        """
        Postprocess the detector's prediction(s) to return a single results dictionary.

        - If a single instance (or batch of instances) was run, the predictions will be
        a length 1 list containing one dictionary, which is returned as is.
        - If N instances were run in an online fashion, the predictions will be a
        length N list of results dictionaries, which are merged into a single
        dictionary containing data lists of length N.
        """
        data: Dict[str, list] = {key: [] for key in pred[0]["data"].keys()}
        for i, pred_i in enumerate(pred):
            for key in data:
                data[key].append(pred_i["data"][key])
        y = {"data": data, "meta": pred[0]["meta"]}
        return y

    @property
    def _should_save_state(self) -> bool:
        return (
            self._online
            and self._model.t % self._ad_settings.state_save_freq == 0
            and self._model.t > 0
        )

    def _save_state(self) -> None:
        # The detector should have a save_state method, but double-check...
        if hasattr(self._model, "save_state"):
            try:
                self._model.save_state(os.path.join(self._model_uri, "state"))
            except Exception as e:
                raise MLServerError(
                    f"Error whilst attempting to save state for model "
                    f"{self._settings.name}: {e}"
                ) from e
        else:
            logger.warning(
                "Attempting to save state but detector doesn't have save_state method."
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
