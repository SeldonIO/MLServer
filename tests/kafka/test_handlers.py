import orjson

from mlserver.types import InferenceResponse
from mlserver.kafka.handlers import KafkaHandlers, KafkaMessage


async def test_infer(kafka_handlers: KafkaHandlers, kafka_request: KafkaMessage):
    kafka_response = await kafka_handlers.infer(kafka_request)

    assert kafka_response.key == kafka_request.key
    assert "Ce-Id" in kafka_response.headers
    assert kafka_response.headers["Ce-Id"] == kafka_response.key
    assert "Ce-Type" in kafka_response.headers
    assert kafka_response.headers["Ce-Type"] == "io.seldon.serving.inference.response"

    parsed = orjson.loads(kafka_response.value)
    inference_response = InferenceResponse(**parsed)
    assert len(inference_response.outputs) == 1
