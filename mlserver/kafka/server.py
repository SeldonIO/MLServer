from mlserver.errors import MLServerError
from enum import Enum
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from aiokafka.errors import ConsumerStoppedError

from ..handlers import DataPlane
from ..settings import Settings
from ..model import MLModel

from .logging import logger
from .utils import encode_headers, decode_headers
from .handlers import KafkaHandlers
from .message import KafkaMessage


# TODO: Explore implementing custom handler
class KafkaMethodTypes(Enum):
    infer = "infer"


class KafkaServer:
    def __init__(self, settings: Settings, data_plane: DataPlane):
        self._settings = settings
        self._handlers = KafkaHandlers(data_plane)

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

        await self._consumer.start()
        await self._producer.start()

        logger.info(
            f"Kafka server consuming messages from {self._settings.kafka_servers}."
        )
        try:
            await self._consumer_loop()
        except ConsumerStoppedError:
            logger.info(
                "Stopped consuming messages from topic "
                f"{self._settings.kafka_topic_input}"
            )

    async def _consumer_loop(self):
        async for request in self._consumer:
            try:
                await self._process_request(request)
            except MLServerError as err:
                logger.exception(f"ERROR {err.status_code} - {str(err)}")
            except Exception as err:
                logger.exception(f"ERROR 500 - {str(err)}")

    async def _process_request(self, request):
        request_headers = decode_headers(request.headers)

        # TODO: Define headers as cloudevent headers
        # TODO: DEfine standard "method header" and decide values
        # Default if not set is assume inference request
        request_method = request_headers.get("mlserver-method", KafkaMethodTypes.infer)

        # TODO: Move logic to KafkaRouter (Also to implement cutom handlers modularly)
        if request_method != KafkaMethodTypes.infer:
            raise MLServerError(f"Invalid request method: {request_method}")

        kafka_request = KafkaMessage(
            key=request.key, value=request.value, headers=request_headers
        )
        kafka_response = await self._handlers.infer(kafka_request)

        response_headers = encode_headers(kafka_response.headers)

        await self._producer.send_and_wait(
            self._settings.kafka_topic_output,
            key=kafka_response.key.encode("utf-8"),  # type: ignore
            value=kafka_response.value.encode("utf-8"),
            headers=response_headers,
        )
        logger.info(f"Processed message of type '{request_method}'")

    async def stop(self, sig: int = None):
        logger.info("Waiting for Kafka server shutdown")
        await self._consumer.stop()
        await self._producer.stop()
        logger.info("Kafka server shutdown complete")
