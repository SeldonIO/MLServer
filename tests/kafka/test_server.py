import asyncio
import pytest

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

from mlserver.types import InferenceResponse
from mlserver.settings import Settings
from mlserver.cloudevents import CLOUDEVENTS_HEADER_ID
from mlserver.kafka.handlers import KafkaMessage, MLSERVER_MODEL_NAME_HEADER


async def test_infer(
    kafka_producer: AIOKafkaProducer,
    kafka_consumer: AIOKafkaConsumer,
    kafka_settings: Settings,
    kafka_request: KafkaMessage,
):
    await kafka_producer.send_and_wait(
        kafka_settings.kafka_topic_input,
        kafka_request.encoded_value,
        headers=kafka_request.encoded_headers,
    )

    res = await asyncio.wait_for(kafka_consumer.getone(), 2)
    kafka_msg = KafkaMessage.from_kafka_record(res)

    inference_response = InferenceResponse(**kafka_msg.value)

    assert CLOUDEVENTS_HEADER_ID in kafka_msg.headers
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
        kafka_request.encoded_value,
        headers=kafka_request.encoded_headers,
    )

    # NOTE: Errors are not sent back to the client. Instead, the server won't
    # return any response.
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(kafka_consumer.getone(), 0.5)
