import orjson
import asyncio

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

from mlserver.types import InferenceRequest
from mlserver.settings import Settings, ModelSettings
from mlserver.kafka.server import KafkaServer
from mlserver.kafka.utils import encode_headers


async def test_infer(
    kafka_producer: AIOKafkaProducer,
    kafka_consumer: AIOKafkaConsumer,
    settings: Settings,
    sum_model_settings: ModelSettings,
    inference_request: InferenceRequest,
):
    headers = encode_headers(
        {
            "mlserver-model": sum_model_settings.name,
        }
    )
    payload = orjson.dumps(inference_request.dict())
    res = await kafka_producer.send_and_wait(
        settings.kafka_topic_input,
        payload,
        headers=list(headers.items()),
    )

    msg = await asyncio.wait_for(kafka_consumer.getone(), 0.5)

    breakpoint()
    print(msg)
