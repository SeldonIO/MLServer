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
    NumpyEncoder,
    SUPPORTED_OPTIMUM_TASKS,
)
from mlserver_huggingface.codecs import MultiStringRequestCodec
from transformers.pipelines import SUPPORTED_TASKS
from mlserver.logging import logger


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
        print("loading model...")
        await asyncio.get_running_loop().run_in_executor(
            None, load_pipeline_from_settings, self.hf_settings
        )
        print("(re)loading model...")
        # Now we load the cached model which should not block asyncio
        self._model = load_pipeline_from_settings(self.hf_settings)
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
        kwargs = self.decode_request(payload, default_codec=MultiStringRequestCodec)

        args = kwargs.pop("args", None)

        X = kwargs.pop("array_inputs", None)
        if X is not None:
            args = [list(X)] + args
        if args is None:
            prediction = self._model(**kwargs)
        else:
            prediction = self._model(args, **kwargs)

        logger.debug("Prediction %s", prediction)

        # TODO: Convert hf output to v2 protocol, for now we use to_json
        if isinstance(prediction, dict):
            str_out = [json.dumps(prediction, cls=NumpyEncoder)]
        else:
            str_out = [json.dumps(pred, cls=NumpyEncoder) for pred in prediction]
        prediction_encoded = StringCodec.encode_output(payload=str_out, name="output")

        return InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            outputs=[prediction_encoded],
        )
