import pytest
import orjson
import docker
import asyncio
import logging

from aiokafka import AIOKafkaClient, AIOKafkaProducer, AIOKafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic
from docker.client import DockerClient

from mlserver.types import InferenceRequest
from mlserver.utils import generate_uuid, install_uvloop_event_loop
from mlserver.settings import Settings, ModelSettings
from mlserver.handlers import DataPlane
from mlserver.kafka.server import KafkaServer
from mlserver.kafka.logging import loggerName
from mlserver.kafka.handlers import (
    KafkaMessage,
    KafkaHandlers,
    MLSERVER_MODEL_NAME_HEADER,
)

from ..utils import get_available_port

logger = logging.getLogger(f"{loggerName}.test")


async def _wait_until_ready(kafka_server: str):
    has_started = False
    attempts_left = 5
    while not has_started and attempts_left > 0:
        try:
            kafka_client = AIOKafkaClient(bootstrap_servers=kafka_server)
            await kafka_client.bootstrap()
            await kafka_client.close()
            logger.debug(
                f"Kafka Cluster has now started and can be accessed at {kafka_server}"
            )
            has_started = True
        except Exception:
            attempts_left -= 1
            if attempts_left == 0:
                logger.exception(f"There was an error starting the Kafka cluster")
                raise

            await asyncio.sleep(2)


def _create_test_topics(settings: Settings):
    admin_client = KafkaAdminClient(bootstrap_servers=settings.kafka_servers)

    input_topic = NewTopic(
        name=settings.kafka_topic_input,
        num_partitions=1,
        replication_factor=1,
    )
    output_topic = NewTopic(
        name=settings.kafka_topic_output,
        num_partitions=1,
        replication_factor=1,
    )
    admin_client.create_topics(new_topics=[input_topic, output_topic])


@pytest.fixture(scope="session")
def event_loop():
    # NOTE: We need to override the `event_loop` fixture to change its scope to
    # `session`, so that it can be used downstream on other `session`-scoped
    # fixtures
    install_uvloop_event_loop()
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def docker_client() -> DockerClient:
    return docker.from_env()


@pytest.fixture(scope="session")
def kafka_network(docker_client: DockerClient) -> str:
    kafka_network = "kafka"
    network = docker_client.networks.create(name=kafka_network)

    yield kafka_network

    network.remove()


@pytest.fixture(scope="session")
def zookeeper(docker_client: DockerClient, kafka_network: str) -> str:
    zookeeper_port = get_available_port()
    container = docker_client.containers.run(
        name="zookeeper",
        image="confluentinc/cp-zookeeper:latest",
        ports={
            f"{zookeeper_port}/tcp": str(zookeeper_port),
        },
        environment={
            "ZOOKEEPER_CLIENT_PORT": str(zookeeper_port),
            "ZOOKEEPER_TICK_TIME": "2000",
        },
        network=kafka_network,
        detach=True,
    )

    yield f"zookeeper:{zookeeper_port}"

    container.remove(force=True)


@pytest.fixture(scope="session")
async def kafka(docker_client: DockerClient, zookeeper: str, kafka_network: str) -> str:
    kafka_port = get_available_port()
    container = docker_client.containers.run(
        name="kafka",
        image="confluentinc/cp-kafka:latest",
        ports={
            f"{kafka_port}/tcp": str(kafka_port),
        },
        environment={
            "KAFKA_ZOOKEEPER_CONNECT": zookeeper,
            "KAFKA_ADVERTISED_LISTENERS": f"PLAINTEXT://kafka:9092,PLAINTEXT_HOST://localhost:{kafka_port}",
            "KAFKA_LISTENER_SECURITY_PROTOCOL_MAP": "PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT",
            "KAFKA_INTER_BROKER_LISTENER_NAME": "PLAINTEXT",
        },
        network=kafka_network,
        detach=True,
    )

    kafka_server = f"localhost:{kafka_port}"

    try:
        # Wait until Kafka server is healthy
        await _wait_until_ready(kafka_server)
        yield kafka_server
    except:
        raise e
    finally:
        # Ensure we always remove the container
        container.remove(force=True)


@pytest.fixture
async def kafka_producer(settings: Settings) -> AIOKafkaProducer:
    producer = AIOKafkaProducer(bootstrap_servers=settings.kafka_servers)
    await producer.start()

    yield producer

    await producer.stop()


@pytest.fixture
async def kafka_consumer(settings: Settings) -> AIOKafkaConsumer:
    consumer = AIOKafkaConsumer(
        settings.kafka_topic_output, bootstrap_servers=settings.kafka_servers
    )
    await consumer.start()

    yield consumer

    await consumer.stop()


@pytest.fixture
def settings(settings: Settings, kafka: str) -> Settings:
    settings.kafka_enabled = True
    settings.kafka_servers = kafka
    return settings


@pytest.fixture
async def kafka_server(settings: Settings, data_plane: DataPlane) -> KafkaServer:
    _create_test_topics(settings)
    server = KafkaServer(settings, data_plane)

    server_task = asyncio.create_task(server.start())
    yield server

    await server.stop()
    await server_task


@pytest.fixture
def kafka_request(
    sum_model_settings: ModelSettings, inference_request: InferenceRequest
) -> KafkaMessage:
    return KafkaMessage(
        key=generate_uuid(),
        value=orjson.dumps(inference_request.dict()),
        headers={MLSERVER_MODEL_NAME_HEADER: sum_model_settings.name},
    )


@pytest.fixture
def kafka_handlers(data_plane: DataPlane) -> KafkaHandlers:
    return KafkaHandlers(data_plane)
