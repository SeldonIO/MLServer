import mlflow

from io import StringIO
from fastapi import Depends, Header, Request, Response

from mlflow.version import VERSION
from mlflow.exceptions import MlflowException
from mlflow.pyfunc.scoring_server import (
    CONTENT_TYPES,
    CONTENT_TYPE_CSV,
    CONTENT_TYPE_JSON,
    parse_csv_input,
    infer_and_parse_json_input,
    predictions_to_json,
)

from mlserver.types import InferenceRequest, InferenceResponse
from mlserver.model import MLModel
from mlserver.utils import get_model_uri
from mlserver.handlers import custom_handler
from mlserver.errors import InferenceError
from mlserver.settings import ModelParameters
from mlserver.logging import logger

from .codecs import TensorDictCodec
from .metadata import (
    to_metadata_tensors,
    to_model_content_type,
    DefaultInputPrefix,
    DefaultOutputPrefix,
)


async def _get_raw_body(request: Request) -> str:
    raw_data = await request.body()
    return raw_data.decode("utf-8")


class MLflowRuntime(MLModel):
    """
    Implementation of the MLModel interface to load and serve `scikit-learn`
    models persisted with `joblib`.
    """

    # TODO: Decouple from REST
    @custom_handler(rest_path="/ping", rest_method="GET")
    async def ping(self) -> str:
        """
        This custom handler is meant to mimic the behaviour of the existing
        health endpoint in MLflow's local dev server.
        For details about its implementation, please consult the original
        implementation in the MLflow repository:

            https://github.com/mlflow/mlflow/blob/master/mlflow/pyfunc/scoring_server/__init__.py
        """
        return "\n"

    @custom_handler(rest_path="/health", rest_method="GET")
    async def health(self) -> str:
        """
        This custom handler is meant to mimic the behaviour of the existing
        health endpoint in MLflow's local dev server.
        For details about its implementation, please consult the original
        implementation in the MLflow repository:

            https://github.com/mlflow/mlflow/blob/master/mlflow/pyfunc/scoring_server/__init__.py
        """
        return "\n"

    # TODO: Decouple from REST
    @custom_handler(rest_path="/version", rest_method="GET")
    async def mlflow_version(self) -> str:
        """
        This custom handler is meant to mimic the behaviour of the existing
        version endpoint in MLflow's local dev server.
        For details about its implementation, please consult the original
        implementation in the MLflow repository:

            https://github.com/mlflow/mlflow/blob/master/mlflow/pyfunc/scoring_server/__init__.py
        """
        return VERSION

    # TODO: Decouple from REST
    @custom_handler(rest_path="/invocations")
    async def invocations(
        self,
        raw_body: str = Depends(_get_raw_body),
        content_type: str = Header(default=""),
    ) -> Response:
        """
        This custom handler is meant to mimic the behaviour of the existing
        scoring server in MLflow.
        For details about its implementation, please consult the original
        implementation in the MLflow repository:

            https://github.com/mlflow/mlflow/blob/master/mlflow/pyfunc/scoring_server/__init__.py
        """
        # Content-Type can include other attributes like CHARSET
        # Content-type RFC: https://datatracker.ietf.org/doc/html/rfc2045#section-5.1
        # TODO: Suport ";" in quoted parameter values
        type_parts = content_type.split(";")
        type_parts = list(map(str.strip, type_parts))
        mime_type = type_parts[0]
        parameter_value_pairs = type_parts[1:]
        parameter_values = {}
        for parameter_value_pair in parameter_value_pairs:
            (key, _, value) = parameter_value_pair.partition("=")
            parameter_values[key] = value

        charset = parameter_values.get("charset", "utf-8").lower()
        if charset != "utf-8":
            raise InferenceError("The scoring server only supports UTF-8")

        unexpected_content_parameters = set(parameter_values.keys()).difference(
            {"charset"}
        )
        if unexpected_content_parameters:
            err_message = (
                f"Unrecognized content type parameters: "
                f"{', '.join(unexpected_content_parameters)}."
            )
            raise InferenceError(err_message)

        if mime_type == CONTENT_TYPE_CSV:
            csv_input = StringIO(raw_body)
            data = parse_csv_input(csv_input=csv_input, schema=self._input_schema)
        elif mime_type == CONTENT_TYPE_JSON:
            data = infer_and_parse_json_input(raw_body, self._input_schema)
        else:
            err_message = (
                "This predictor only supports the following content types, "
                f"{CONTENT_TYPES}. Got '{content_type}'."
            )
            raise InferenceError(err_message)

        try:
            raw_predictions = self._model.predict(data)
        except MlflowException as e:
            raise InferenceError(e.message)
        except Exception:
            error_message = (
                "Encountered an unexpected error while evaluating the model. Verify"
                " that the serialized input Dataframe is compatible with the model for"
                " inference."
            )
            raise InferenceError(error_message)

        result = StringIO()
        predictions_to_json(raw_predictions, result)
        return Response(content=result.getvalue(), media_type="application/json")

    async def load(self) -> bool:
        # TODO: Log info message
        model_uri = await get_model_uri(self._settings)
        self._model = mlflow.pyfunc.load_model(model_uri)

        self._input_schema = self._model.metadata.get_input_schema()
        self._signature = self._model.metadata.signature
        self._sync_metadata()

        return True

    def _sync_metadata(self) -> None:
        # Update metadata from model signature (if present)
        if self._signature is None:
            return

        if self.inputs:
            logger.warning("Overwriting existing inputs metadata with model signature")

        self.inputs = to_metadata_tensors(
            schema=self._signature.inputs, prefix=DefaultInputPrefix
        )

        if self.outputs:
            logger.warning("Overwriting existing outputs metadata with model signature")

        self.outputs = to_metadata_tensors(
            schema=self._signature.outputs, prefix=DefaultOutputPrefix
        )

        if not self._settings.parameters:
            self._settings.parameters = ModelParameters()

        if self._settings.parameters.content_type:
            logger.warning(
                "Overwriting existing request-level content type with model signature"
            )

        self._settings.parameters.content_type = to_model_content_type(
            schema=self._signature.inputs
        )

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        decoded_payload = self.decode_request(payload)
        model_output = self._model.predict(decoded_payload)
        return self.encode_response(model_output, default_codec=TensorDictCodec)
