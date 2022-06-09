from mlserver.kafka.server import KafkaServer


async def test_start(kafka_server: KafkaServer):
    breakpoint()
    print(kafka_server)
