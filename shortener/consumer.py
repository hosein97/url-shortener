import logging
import json
import pika

from config.messaging.rabbitmq import get_connection
from config.redis import redis_client
from shortener.services import increment_clicks


logger = logging.getLogger(__name__)


def callback(ch, method, properties, body):

    try:
        event = json.loads(body.decode())

        short_code = event["short_code"]
        
        increment_clicks(short_code)
        
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        
        logger.exception(
            "Processing click event failed"
        )
        # optional: requeue or dead-letter later
        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=False
        )


def start_consumer():

    connection = get_connection()

    channel = connection.channel()

    channel.exchange_declare(
        exchange="clicks",
        exchange_type="fanout",
        durable=True,
    )

    channel.queue_declare(
        queue="shortener.clicks",
        durable=True,
    )

    channel.queue_bind(
        exchange="clicks",
        queue="shortener.clicks",
    )

    channel.basic_consume(
        queue="shortener.clicks",
        on_message_callback=callback,
    )
    
    logger.info("Waiting for click events...")

    channel.start_consuming()

