
import os
import time
import logging
from pika import PlainCredentials, BlockingConnection, ConnectionParameters


def digest(ch, method, properties, body):
    _logger.info("ch: %s:%s | method: %s:%s | properties: %s:%s | body: %s:%s",
                        ch, type(ch), method, type(method), properties, type(properties), body, type(body))
    _logger.info("Message payload: %s", body)


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
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
channel.basic_consume(
    queue='telemetry',
    auto_ack=True,
    on_message_callback=digest
)
channel.start_consuming()
_logger.info("AMQP connection established with broker %s:%s", host, port)

while True:
    time.sleep(1)
