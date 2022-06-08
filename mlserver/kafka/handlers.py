import orjson

from typing import Dict
from aiokafka.record.default_records import DefaultRecord
from pydantic import BaseModel

from ..utils import insert_headers, extract_headers
from ..types import InferenceRequest
from ..handlers import DataPlane


class KafkaMessage(BaseModel):
    key: str
    value: str
    headers: Dict[str, str]


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
        # TODO: Check and fail if headers are not set (or handle defaults)
        model_name = request.headers["mlserver-model"]
        model_version = request.headers.get("mlserver-version", None)
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
