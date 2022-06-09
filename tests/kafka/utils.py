import asyncio
import logging

from aiokafka import AIOKafkaClient
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

from mlserver.settings import Settings
from mlserver.kafka.logging import loggerName

logger = logging.getLogger(f"{loggerName}.test")


async def wait_until_ready(kafka_server: str):
    has_started = False
    attempts_left = 5
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


async def _wait_for_topics(admin_client: KafkaAdminClient, settings: Settings) -> bool:
    topic_names = [settings.kafka_topic_input, settings.kafka_topic_output]

    topics_exist = False
    attempts_left = 5
    while not topics_exist and attempts_left > 0:
        topics = admin_client.list_topics()
        topics_exist = all([topic_name in topics for topic_name in topic_names])
        if topics_exist:
            return True

        attempts_left -= 1
        await asyncio.sleep(0.5)

    return False


async def create_test_topics(settings: Settings):
    admin_client = KafkaAdminClient(bootstrap_servers=settings.kafka_servers)

    logger.debug(
        f"Creating topics '{settings.kafka_topic_input}' and "
        f"'{settings.kafka_topic_output}'..."
    )

    topic_names = [settings.kafka_topic_input, settings.kafka_topic_output]
    new_topics = [
        NewTopic(
            name=topic_name,
            num_partitions=1,
            replication_factor=1,
        )
        for topic_name in topic_names
    ]
    try:
        admin_client.create_topics(new_topics=new_topics)
        # Wait for topics to get created
        await _wait_for_topics(admin_client, settings)
        logger.debug(
            f"Topics '{settings.kafka_topic_input}' and "
            f"'{settings.kafka_topic_output}' have been created"
        )
    except TopicAlreadyExistsError:
        pass
    finally:
        admin_client.close()
