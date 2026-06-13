import json
import pika

from config.messaging.rabbitmq import get_connection
from analytics.services import process_click

logger = logging.getLogger(__name__)



QUEUE_NAME = "clicks"


def callback(ch, method, properties, body):

    try:
        event = json.loads(body.decode())

        process_click(event)

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

    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True,
    )

    channel.basic_qos(
        prefetch_count=100
    )

    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback,
    )

    logger.info("Waiting for click events...")

    channel.start_consuming()