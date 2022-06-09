import orjson

from typing import Optional, Tuple

from ..utils import insert_headers, extract_headers
from ..types import InferenceRequest
from ..handlers import DataPlane

from .message import KafkaMessage
from .errors import InvalidMessageHeaders

MLSERVER_MODEL_NAME_HEADER = "mlserver-model"
MLSERVER_MODEL_VERSION_HEADER = "mlserver-version"


class KafkaHandlers:
    def __init__(self, data_plane: DataPlane):
        self._data_plane = data_plane

    async def infer(self, request: KafkaMessage) -> KafkaMessage:
        request_json = orjson.loads(request.value)
        inference_request = InferenceRequest(**request_json)

        # Kafka KEY takes precedence over body ID
        if request.key:
            inference_request.id = request.key

        insert_headers(inference_request, request.headers)

        # TODO: Update header with consistency with other headeres
        model_name, model_version = self._get_model_details(request)
        inference_response = await self._data_plane.infer(
            inference_request, model_name, model_version
        )

        response_value = orjson.dumps(inference_response.dict())
        response_headers = extract_headers(inference_response)
        if response_headers is None:
            response_headers = {}

        return KafkaMessage(
            key=inference_response.id, value=response_value, headers=response_headers
        )

    def _get_model_details(self, request: KafkaMessage) -> Tuple[str, Optional[str]]:
        headers = request.headers

        if MLSERVER_MODEL_NAME_HEADER not in headers:
            raise InvalidMessageHeaders(MLSERVER_MODEL_NAME_HEADER)

        model_name = headers[MLSERVER_MODEL_NAME_HEADER]
        model_version = headers.get(MLSERVER_MODEL_VERSION_HEADER, None)

        return model_name, model_version
