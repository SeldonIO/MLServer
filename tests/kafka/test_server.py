import orjson
import asyncio

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

from mlserver.types import InferenceRequest, InferenceResponse
from mlserver.settings import Settings, ModelSettings
from mlserver.cloudevents import CLOUDEVENTS_HEADER_ID
from mlserver.kafka.server import KafkaServer
from mlserver.kafka.utils import encode_headers, decode_headers
from mlserver.kafka.handlers import KafkaMessage


async def test_infer(
    kafka_producer: AIOKafkaProducer,
    kafka_consumer: AIOKafkaConsumer,
    settings: Settings,
    kafka_request: KafkaMessage,
):
    res = await kafka_producer.send_and_wait(
        settings.kafka_topic_input,
        kafka_request.value.encode("utf-8"),
        headers=encode_headers(kafka_request.headers),
    )

    msg = await asyncio.wait_for(kafka_consumer.getone(), 0.5)

    response_headers = decode_headers(msg.headers)
    inference_response = InferenceResponse(**orjson.loads(msg.value))

    assert CLOUDEVENTS_HEADER_ID in response_headers
    assert len(inference_response.outputs) > 0
