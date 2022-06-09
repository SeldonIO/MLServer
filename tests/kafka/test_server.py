import orjson
import asyncio
import pytest

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

from mlserver.types import InferenceResponse
from mlserver.settings import Settings
from mlserver.cloudevents import CLOUDEVENTS_HEADER_ID
from mlserver.kafka.utils import encode_headers, decode_headers
from mlserver.kafka.handlers import KafkaMessage, MLSERVER_MODEL_NAME_HEADER


async def test_infer(
    kafka_producer: AIOKafkaProducer,
    kafka_consumer: AIOKafkaConsumer,
    kafka_settings: Settings,
    kafka_request: KafkaMessage,
):
    await kafka_producer.send_and_wait(
        kafka_settings.kafka_topic_input,
        kafka_request.value.encode("utf-8"),
        headers=encode_headers(kafka_request.headers),
    )

    msg = await asyncio.wait_for(kafka_consumer.getone(), 0.5)

    response_headers = decode_headers(msg.headers)
    inference_response = InferenceResponse(**orjson.loads(msg.value))

    assert CLOUDEVENTS_HEADER_ID in response_headers
    assert len(inference_response.outputs) > 0


async def test_infer_error(
    kafka_producer: AIOKafkaProducer,
    kafka_consumer: AIOKafkaConsumer,
    kafka_settings: Settings,
    kafka_request: KafkaMessage,
):
    kafka_request.headers[MLSERVER_MODEL_NAME_HEADER] = "non-existing-model"
    await kafka_producer.send_and_wait(
        kafka_settings.kafka_topic_input,
        kafka_request.value.encode("utf-8"),
        headers=encode_headers(kafka_request.headers),
    )

    # NOTE: Errors are not sent back to the client. Instead, the server won't
    # return any response.
    with pytest.raises(asyncio.exceptions.TimeoutError):
        await asyncio.wait_for(kafka_consumer.getone(), 0.5)
