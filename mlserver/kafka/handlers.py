import orjson

from typing import Dict
from aiokafka.record.default_records import DefaultRecord
from pydantic import BaseModel

from ..cloudevents import get_cloudevent_headers
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
        # Kafka KEY takes prescedence over body ID
        request_json = orjson.loads(request.value)

        if request.key:
            request_json["id"] = request.key

        inference_request = InferenceRequest(**request_json)

        # TODO: Update header with consistency with other headeres
        # TODO: Check and fail if headers are not set (or handle defaults)
        model_name = request.headers["mlserver-model"]
        model_version = request.headers.get("mlserver-version", None)
        inference_response = await self._data_plane.infer(
            inference_request, model_name, model_version
        )

        response_value = orjson.dumps(inference_response.dict())

        # TODO: Add cloudevent headers
        response_headers = get_cloudevent_headers(
            inference_response.id, "io.seldon.serving.inference.response"
        )

        return KafkaMessage(
            key=inference_response.id, value=response_value, headers=response_headers
        )
