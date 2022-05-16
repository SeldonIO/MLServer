import json
import asyncio
from mlserver.model import MLModel
from mlserver.settings import ModelSettings
from mlserver.types import (
    InferenceRequest,
    InferenceResponse,
)
from mlserver.codecs import (
    StringCodec,
)
from mlserver_huggingface.common import (
    HuggingFaceSettings,
    parse_parameters_from_env,
    InvalidTranformerInitialisation,
    load_pipeline_from_settings,
)
from mlserver_huggingface.codecs import MultiStringRequestCodec
from transformers.pipelines import SUPPORTED_TASKS
from optimum.pipelines import SUPPORTED_TASKS as SUPPORTED_OPTIMUM_TASKS


class HuggingFaceRuntime(MLModel):
    """Runtime class for specific Huggingface models"""

    def __init__(self, settings: ModelSettings):
        env_params = parse_parameters_from_env()
        if not env_params and (
            not settings.parameters or not settings.parameters.extra
        ):
            raise InvalidTranformerInitialisation(
                500,
                "Settings parameters not provided via config file nor env variables",
            )

        extra = env_params or settings.parameters.extra  # type: ignore
        self.hf_settings = HuggingFaceSettings(**extra)  # type: ignore

        if self.hf_settings.task not in SUPPORTED_TASKS:
            raise InvalidTranformerInitialisation(
                500,
                (
                    f"Invalid transformer task: {self.hf_settings.task}."
                    f" Available tasks: {SUPPORTED_TASKS.keys()}"
                ),
            )

        if self.hf_settings.optimum_model:
            if self.hf_settings.task not in SUPPORTED_OPTIMUM_TASKS:
                raise InvalidTranformerInitialisation(
                    500,
                    (
                        f"Invalid transformer task for "
                        f"OPTIMUM model: {self.hf_settings.task}. "
                        f"Supported Optimum tasks: {SUPPORTED_OPTIMUM_TASKS.keys()}"
                    ),
                )

        super().__init__(settings)

    async def load(self) -> bool:
        # Loading & caching pipeline in asyncio loop to avoid blocking
        await asyncio.get_running_loop().run_in_executor(
            None, load_pipeline_from_settings, self.hf_settings
        )
        # Now we load the cached model which should not block asyncio
        self._model = load_pipeline_from_settings(self.hf_settings)
        self.ready = True
        return self.ready

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        """
        TODO
        """

        # TODO: convert and validate?
        kwargs = self.decode_request(payload, default_codec=MultiStringRequestCodec)

        args = []
        if "args" in kwargs:
            args = kwargs["args"]
            del kwargs["args"]
        prediction = self._model(*args, **kwargs)

        # TODO: Convert hf output to v2 protocol, for now we use to_json
        prediction_encoded = StringCodec.encode(
            payload=[json.dumps(prediction)], name="output"
        )

        return InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            outputs=[prediction_encoded],
        )
