from mlserver.errors import MLServerError
from typing import Dict
import logging
import orjson
from enum import Enum
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from ..cloudevents import get_cloudevent_headers
from ..handlers import DataPlane, ModelRepositoryHandlers
from ..settings import Settings
from ..types import InferenceRequest
from ..model import MLModel
from ..utils import logger


class KafkaServer:
    def __init__(
        self,
        settings: Settings,
        data_plane: DataPlane,
        model_repository_handlers: ModelRepositoryHandlers,
    ):
        self._settings = settings
        self._data_plane = data_plane
        self._model_repository_handlers = model_repository_handlers

    def _create_server(self):
        self._consumer = AIOKafkaConsumer(
            self._settings.kafka_topic_input,
            bootstrap_servers=self._settings.kafka_servers,
        )
        self._producer = AIOKafkaProducer(
            bootstrap_servers=self._settings.kafka_servers
        )

    async def add_custom_handlers(self, model: MLModel):
        # TODO: Implement
        pass

    async def delete_custom_handlers(self, model: MLModel):
        # TODO: Implement
        pass

    async def start(self):
        self._create_server()

        # TODO: Move logic to KafkaRouter (Also to implement cutom handlers modularly)
        await self._consumer.start()
        await self._producer.start()
        # TODO: Catch or ensure parent function catches and stops server
        async for request in self._consumer:
            try:
                # Logging without converting to string for efficiency if no DEBUG
                logger.debug(request.value)
                request_key = request.key
                request_json = orjson.loads(request.value)
                request_headers: Dict[str, str] = {
                    k: v.decode("utf-8") for k, v in request.headers
                }
                # TODO: Define headers as cloudevent headers
                # TODO: DEfine standard "method header" and decide values
                request_method = request_headers.get("mlserver-method")

                # TODO: Explore implementing custom handler
                class KafkaMethodTypes(Enum):
                    infer = "infer"

                # DEfault if not set is assume inference request
                if not request_method or request_method == KafkaMethodTypes.infer:
                    # Kafka KEY takes prescedence over body ID
                    if request_key:
                        request_json["id"] = request_key
                    infer_request = InferenceRequest(**request_json)
                    # TODO: Update header with consistency with other headeres
                    # TODO: Check and fail if headers are not set (or handle defaults)
                    infer_model = request_headers["mlserver-model"]
                    infer_version = request_headers["mlserver-version"]
                    infer_response = await self._data_plane.infer(
                        infer_request, infer_model, infer_version
                    )
                    response_key = infer_response.id
                    response_value = orjson.dumps(infer_response.dict())
                else:
                    raise MLServerError(f"Invalid request method: {request_method}")

                # TODO: Add cloudevent headers
                response_headers = get_cloudevent_headers(
                    response_key, "io.seldon.serving.inference.response"
                )
                response_headers_kafka = [(k, v.encode("utf-8"),) for k, v in response_headers.items()]

                await self._producer.send_and_wait(
                    self._settings.kafka_topic_output,
                    key=response_key.encode("utf-8"),  # type: ignore
                    value=response_value,
                    headers=response_headers_kafka,
                )
            except Exception:
                logger.exception("Kafka Processed Request - 500 ERROR")
            else:
                logger.info("Kafka Processed Request - 200 OK")

    async def stop(self):
        await self._consumer.stop()
        await self._producer.stop()
