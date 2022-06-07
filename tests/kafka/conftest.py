import pytest
import orjson

from mlserver.types import InferenceRequest
from mlserver.utils import generate_uuid
from mlserver.settings import ModelSettings
from mlserver.handlers import DataPlane
from mlserver.kafka.handlers import KafkaMessage, KafkaHandlers


@pytest.fixture
def kafka_request(
    sum_model_settings: ModelSettings, inference_request: InferenceRequest
) -> KafkaMessage:
    return KafkaMessage(
        key=generate_uuid(),
        value=orjson.dumps(inference_request.dict()),
        headers={"mlserver-model": sum_model_settings.name},
    )


@pytest.fixture
def kafka_handlers(data_plane: DataPlane) -> KafkaHandlers:
    return KafkaHandlers(data_plane)
