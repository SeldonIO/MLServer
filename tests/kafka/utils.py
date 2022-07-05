import logging

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    wait_fixed,
    retry_if_result,
)
from typing import List
from aiokafka import AIOKafkaClient
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

from mlserver.kafka.logging import loggerName

logger = logging.getLogger(f"{loggerName}.test")


@retry(stop=stop_after_attempt(20), wait=wait_exponential(min=0, max=4))
async def bootstrap(kafka_server: str):
    logger.debug(f"Starting Kafka cluster at {kafka_server}...")
    kafka_client = AIOKafkaClient(bootstrap_servers=kafka_server)
    await kafka_client.bootstrap()
    await kafka_client.close()
    logger.debug(f"Kafka cluster has now started and can be accessed at {kafka_server}")


def _is_false(v: bool) -> bool:
    return not v


@retry(
    stop=stop_after_attempt(5), wait=wait_fixed(0.5), retry=retry_if_result(_is_false)
)
async def _check_topics(admin_client: KafkaAdminClient, topics: List[str]) -> bool:
    existing_topics = admin_client.list_topics()
    return all([topic in existing_topics for topic in topics])


async def create_test_topics(admin_client: KafkaAdminClient, topics: List[str]):
    logger.debug(f"Creating topics {topics} ...")

    new_topics = [
        NewTopic(
            name=topic,
            num_partitions=1,
            replication_factor=1,
        )
        for topic in topics
    ]
    try:
        admin_client.create_topics(new_topics=new_topics)
        # Wait for topics to get created
        await _check_topics(admin_client, topics)
        logger.debug(f"Topics {topics} have been created")
    except TopicAlreadyExistsError:
        pass
    finally:
        admin_client.close()
