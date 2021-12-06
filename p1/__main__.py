
import os
import json
import time
import logging
from typing import Any, Dict
from pika import PlainCredentials, BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel


def publish(channel: BlockingChannel, route: str, body: Dict[str, Any]) -> None:
    _logger.info("Message payload: %s", body)
    channel.basic_publish(
        exchange='device',
        routing_key=route,
        body=json.dumps(body)
    )


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
# RMQ Event config
host = os.environ['RABBITMQ_ADDR'].split(':')[0]
port = int(os.environ['RABBITMQ_ADDR'].split(':')[1])
_logger = logging.getLogger(__name__)
_logger.debug("Creating rabbitmq connection to host: %s port: %s", host, port)
credentials = PlainCredentials(
    username="microservice",
    password="microservice",
    erase_on_connect=True
)
connection = BlockingConnection(
    ConnectionParameters(
        host=host,
        port=port,
        virtual_host='/',
        credentials=credentials
    )
)
channel = connection.channel()
_logger.info("AMQP connection established with broker %s:%s", host, port)

while True:
    publish(channel, 'device.telemetry', {'type': 1})
    time.sleep(1)
