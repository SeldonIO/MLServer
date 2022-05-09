import json
from mlserver.codecs import (
    StringCodec,
)
from mlserver.codecs.string import StringRequestCodec
from mlserver.model import MLModel
from mlserver.settings import ModelSettings
from mlserver.types import (
    InferenceRequest,
    InferenceResponse,
)
from mlserver_huggingface.common import (
    HuggingFaceSettings,
    HUGGINGFACE_PARAMETERS_TAG,
    parse_parameters_from_env,
    InvalidTranformerInitialisation,
    SUPPORTED_OPTIMIZED_TASKS,
)
from transformers.pipelines.base import Pipeline
from transformers.pipelines import pipeline, SUPPORTED_TASKS
from transformers import AutoTokenizer


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
            if self.hf_settings.task not in SUPPORTED_OPTIMIZED_TASKS:
                raise InvalidTranformerInitialisation(
                    500,
                    (
                        f"Invalid transformer task for "
                        f"OPTIMUM model: {self.hf_settings.task}. "
                        f"Supported Optimum tasks: {SUPPORTED_OPTIMIZED_TASKS.keys()}"
                    ),
                )

        super().__init__(settings)

    async def load(self) -> bool:
        self._model = self._load_from_settings()
        self.ready = True
        return self.ready

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        """
        TODO
        """

        # TODO: convert and validate?
        input_data = self.decode_request(payload, default_codec=StringRequestCodec)

        params = payload.parameters
        kwarg_params = dict()
        if params is not None:
            params_dict = params.dict()
            if HUGGINGFACE_PARAMETERS_TAG in params_dict:
                kwarg_params = params_dict[HUGGINGFACE_PARAMETERS_TAG]

        prediction = self._model(input_data, **kwarg_params)

        # TODO: Convert hf output to v2 protocol, for now we use to_json
        prediction_encoded = StringCodec.encode(
            payload=[json.dumps(prediction)], name="huggingface"
        )

        return InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            outputs=[prediction_encoded],
        )

    def _load_from_settings(self) -> Pipeline:
        """
        TODO
        """
        # TODO: Support URI for locally downloaded artifacts
        # uri = model_parameters.uri
        model = self.hf_settings.pretrained_model
        tokenizer = self.hf_settings.pretrained_tokenizer

        if model and not tokenizer:
            tokenizer = model

        if self.hf_settings.optimum_model:
            optimum_class = SUPPORTED_OPTIMIZED_TASKS[self.hf_settings.task]
            model = optimum_class.from_pretrained(
                self.hf_settings.pretrained_model, from_transformers=True
            )
            tokenizer = AutoTokenizer.from_pretrained(tokenizer)

        pp = pipeline(
            self.hf_settings.task,
            model=model,
            tokenizer=tokenizer,
        )
        return pp
