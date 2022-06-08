import orjson
import pytest

from mlserver.cloudevents import (
    CloudEventsTypes,
    CLOUDEVENTS_HEADER_TYPE,
    CLOUDEVENTS_HEADER_ID,
)
from mlserver.types import InferenceResponse
from mlserver.kafka.handlers import (
    KafkaHandlers,
    KafkaMessage,
    MLSERVER_MODEL_NAME_HEADER,
)
from mlserver.kafka.errors import InvalidMessageHeaders


async def test_infer(kafka_handlers: KafkaHandlers, kafka_request: KafkaMessage):
    kafka_response = await kafka_handlers.infer(kafka_request)

    assert kafka_response.key == kafka_request.key
    assert CLOUDEVENTS_HEADER_ID in kafka_response.headers
    assert kafka_response.headers[CLOUDEVENTS_HEADER_ID] == kafka_response.key
    assert CLOUDEVENTS_HEADER_TYPE in kafka_response.headers
    assert (
        kafka_response.headers[CLOUDEVENTS_HEADER_TYPE]
        == CloudEventsTypes.Response.value
    )

    parsed = orjson.loads(kafka_response.value)
    inference_response = InferenceResponse(**parsed)
    assert len(inference_response.outputs) == 1


async def test_infer_error(kafka_handlers: KafkaHandlers, kafka_request: KafkaMessage):
    del kafka_request.headers[MLSERVER_MODEL_NAME_HEADER]

    with pytest.raises(InvalidMessageHeaders):
        await kafka_handlers.infer(kafka_request)
