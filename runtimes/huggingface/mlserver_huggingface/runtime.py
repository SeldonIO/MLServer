import asyncio
from mlserver.model import MLModel
from mlserver.settings import ModelSettings
from mlserver.types import (
    InferenceRequest,
    InferenceResponse,
)
from mlserver_huggingface.common import (
    HuggingFaceSettings,
    parse_parameters_from_env,
    InvalidTranformerInitialisation,
    load_pipeline_from_settings,
)
from mlserver_huggingface.codecs import HuggingfaceRequestCodec
from transformers.pipelines import SUPPORTED_TASKS
from optimum.pipelines import SUPPORTED_TASKS as SUPPORTED_OPTIMUM_TASKS
from mlserver.logging import logger
from mlserver_huggingface.metadata import METADATA


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

        if settings.max_batch_size != self.hf_settings.batch_size:
            logger.warning(
                f"hf batch_size: {self.hf_settings.batch_size} is different "
                f"from MLServer max_batch_size: {settings.max_batch_size}"
            )

        super().__init__(settings)

    async def load(self) -> bool:
        # Loading & caching pipeline in asyncio loop to avoid blocking
        print("=" * 80)
        print(self.hf_settings.task_name)
        print("loading model...")
        await asyncio.get_running_loop().run_in_executor(
            None, load_pipeline_from_settings, self.hf_settings
        )
        print("(re)loading model...")
        # Now we load the cached model which should not block asyncio
        self._model = load_pipeline_from_settings(self.hf_settings)
        self._merge_metadata()
        print("model has been loaded!")
        self.ready = True
        return self.ready

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        """
        TODO
        """

        # Adding some logging as hard to debug given the many types of input accepted
        logger.debug("Payload %s", payload)

        # TODO: convert and validate?
        kwargs = self.decode_request(payload, default_codec=HuggingfaceRequestCodec)
        args = kwargs.pop("args", [])

        array_inputs = kwargs.pop("array_inputs", [])
        if array_inputs:
            args = [list(array_inputs)] + args
        prediction = self._model(*args, **kwargs)

        logger.debug("Prediction %s", prediction)

        return self.encode_response(
            payload=prediction, default_codec=HuggingfaceRequestCodec
        )

    def _merge_metadata(self) -> None:
        meta = METADATA.get(self.hf_settings.task)
        if meta:
            self.inputs += meta.get("inputs", [])  # type: ignore
            self.outputs += meta.get("outputs", [])  # type: ignore
