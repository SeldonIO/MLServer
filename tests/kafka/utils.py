import asyncio
import logging

from typing import List
from aiokafka import AIOKafkaClient
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

from mlserver.kafka.logging import loggerName

logger = logging.getLogger(f"{loggerName}.test")


async def wait_until_ready(kafka_server: str):
    has_started = False
    attempts_left = 20
    while not has_started and attempts_left > 0:
        try:
            logger.debug(f"Starting Kafka cluster at {kafka_server}...")
            kafka_client = AIOKafkaClient(bootstrap_servers=kafka_server)
            await kafka_client.bootstrap()
            await kafka_client.close()
            logger.debug(
                f"Kafka cluster has now started and can be accessed at {kafka_server}"
            )
            has_started = True
        except Exception:
            attempts_left -= 1
            if attempts_left == 0:
                logger.exception("There was an error starting the Kafka cluster")
                raise

            logger.debug(
                f"Kafka cluster has not started yet ({attempts_left} attempts left)"
            )
            await asyncio.sleep(2)


async def _wait_for_topics(admin_client: KafkaAdminClient, topics: List[str]) -> bool:
    topics_exist = False
    attempts_left = 5
    while not topics_exist and attempts_left > 0:
        existing_topics = admin_client.list_topics()
        topics_exist = all([topic in existing_topics for topic in topics])
        if topics_exist:
            return True

        attempts_left -= 1
        await asyncio.sleep(0.5)

    return False


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
        await _wait_for_topics(admin_client, topics)
        logger.debug(f"Topics {topics} have been created")
    except TopicAlreadyExistsError:
        pass
    finally:
        admin_client.close()
