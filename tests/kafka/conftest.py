import pytest
import docker
import asyncio

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from kafka.admin import KafkaAdminClient
from docker.client import DockerClient
from typing import Tuple

from mlserver.types import InferenceRequest
from mlserver.utils import generate_uuid, install_uvloop_event_loop
from mlserver.settings import Settings, ModelSettings
from mlserver.handlers import DataPlane
from mlserver.kafka.server import KafkaServer
from mlserver.kafka.handlers import (
    KafkaHandlers,
    MLSERVER_MODEL_NAME_HEADER,
)
from mlserver.kafka.message import KafkaMessage

from ..utils import get_available_ports

from .utils import create_test_topics, bootstrap


@pytest.fixture(scope="module")
def event_loop():
    # NOTE: We need to override the `event_loop` fixture to change its scope to
    # `module`, so that it can be used downstream on other `module`-scoped
    # fixtures
    install_uvloop_event_loop()
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
def docker_client() -> DockerClient:
    return docker.from_env()


@pytest.fixture(scope="module")
def kafka_network(docker_client: DockerClient) -> str:
    kafka_network = "kafka"
    network = docker_client.networks.create(name=kafka_network)

    yield kafka_network

    network.remove()


@pytest.fixture(scope="module")
def zookeeper(docker_client: DockerClient, kafka_network: str) -> str:
    [zookeeper_port] = get_available_ports()
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


@pytest.fixture(scope="module")
async def kafka(docker_client: DockerClient, zookeeper: str, kafka_network: str) -> str:
    [kafka_port] = get_available_ports()
    container = docker_client.containers.run(
        name="kafka",
        image="confluentinc/cp-kafka:latest",
        ports={
            f"{kafka_port}/tcp": str(kafka_port),
        },
        environment={
            "KAFKA_ZOOKEEPER_CONNECT": zookeeper,
            "KAFKA_ADVERTISED_LISTENERS": (
                f"PLAINTEXT://kafka:9092,PLAINTEXT_HOST://localhost:{kafka_port}"
            ),
            "KAFKA_LISTENER_SECURITY_PROTOCOL_MAP": (
                "PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT"
            ),
            "KAFKA_INTER_BROKER_LISTENER_NAME": "PLAINTEXT",
        },
        network=kafka_network,
        detach=True,
    )

    kafka_server = f"localhost:{kafka_port}"

    try:
        # Wait until Kafka server is healthy
        await bootstrap(kafka_server)
        yield kafka_server
    except Exception:
        raise
    finally:
        # Ensure we always remove the container
        container.remove(force=True)


@pytest.fixture(scope="module")
async def kafka_topics(kafka: str) -> Tuple[str, str]:
    input_topic = "mlserver-input-topic"
    output_topic = "mlserver-output-topic"
    topics = [input_topic, output_topic]

    admin_client = KafkaAdminClient(bootstrap_servers=kafka)
    await create_test_topics(admin_client, topics)

    yield tuple(topics)

    # NOTE: Deleting topics seems to hang for some reason
    #  admin_client.delete_topics(topics=topics, timeout_ms=1000)


@pytest.fixture
def kafka_settings(
    settings: Settings, kafka: str, kafka_topics: Tuple[str, str]
) -> Settings:
    input_topic, output_topic = kafka_topics

    settings.kafka_enabled = True
    settings.kafka_servers = kafka
    settings.kafka_topic_input = input_topic
    settings.kafka_topic_output = output_topic

    return settings


@pytest.fixture
async def kafka_server(kafka_settings: Settings, data_plane: DataPlane) -> KafkaServer:
    server = KafkaServer(kafka_settings, data_plane)

    server_task = asyncio.create_task(server.start())
    # NOTE: The Kafka server doesn't have any health checks, therefore we need
    # to give it some time until it's ready
    await asyncio.sleep(1)

    yield server

    await server.stop()
    await server_task


@pytest.fixture
async def kafka_producer(
    kafka_server: KafkaServer, kafka_settings: Settings
) -> AIOKafkaProducer:
    producer = AIOKafkaProducer(bootstrap_servers=kafka_settings.kafka_servers)
    await producer.start()

    yield producer

    await producer.stop()


@pytest.fixture
async def kafka_consumer(
    kafka_server: KafkaServer, kafka_settings: Settings
) -> AIOKafkaConsumer:
    consumer = AIOKafkaConsumer(
        kafka_settings.kafka_topic_output,
        bootstrap_servers=kafka_settings.kafka_servers,
    )
    await consumer.start()

    yield consumer

    await consumer.stop()


@pytest.fixture
def kafka_request(
    sum_model_settings: ModelSettings, inference_request: InferenceRequest
) -> KafkaMessage:
    return KafkaMessage.from_types(
        key=generate_uuid(),
        value=inference_request,
        headers={MLSERVER_MODEL_NAME_HEADER: sum_model_settings.name},
    )


@pytest.fixture
def kafka_handlers(data_plane: DataPlane) -> KafkaHandlers:
    return KafkaHandlers(data_plane)
