from mlserver.errors import MLServerError
from typing import Dict
import orjson
from enum import Enum
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from ..handlers import DataPlane, ModelRepositoryHandlers
from ..settings import Settings
from ..types import InferenceRequest
from ..model import MLModel

from .logging import logger
from .utils import encode_headers, decode_headers
from .handlers import KafkaHandlers, KafkaMessage

# TODO: Explore implementing custom handler
class KafkaMethodTypes(Enum):
    infer = "infer"


class KafkaServer:
    def __init__(
        self,
        settings: Settings,
        data_plane: DataPlane,
        model_repository_handlers: ModelRepositoryHandlers,
    ):
        self._settings = settings
        self._handlers = KafkaHandlers(data_plane)
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

        logger.info(f"Kafka server consuming from {self._settings.kafka_servers}.")
        await self._consumer_loop()

    async def _consumer_loop(self):
        # TODO: Catch or ensure parent function catches and stops server
        async for request in self._consumer:
            try:
                self._process_request(request)
            except Exception:
                logger.exception("Kafka Processed Request - 500 ERROR")
            else:
                logger.info("Kafka Processed Request - 200 OK")

    async def _process_request(self, request):
        request_headers = decode_headers(request.headers)

        # TODO: Define headers as cloudevent headers
        # TODO: DEfine standard "method header" and decide values
        request_method = request_headers.get("mlserver-method")

        # Default if not set is assume inference request
        if request_method is not None and request_method != KafkaMethodTypes.infer:
            raise MLServerError(f"Invalid request method: {request_method}")

        kafka_request = KafkaMessage(
            key=request.key, value=request.value, headers=request_headers
        )
        kafka_response = await self._handlers.infer(kafka_request)

        response_headers = encode_headers(request_headers)

        await self._producer.send_and_wait(
            self._settings.kafka_topic_output,
            key=kafka_response.key.encode("utf-8"),  # type: ignore
            value=kafka_response.value,
            headers=response_headers,
        )

    async def stop(self, sig: int = None):
        logger.info("Waiting for Kafka server shutdown")
        await self._consumer.stop()
        await self._producer.stop()
        logger.info("Kafka server shutdown complete")
