import pika

from config.messaging.rabbitmq import get_connection
from analytics.services import process_click


QUEUE_NAME = "clicks"


def callback(ch, method, properties, body):

    short_code = body.decode()

    process_click(short_code)

    ch.basic_ack(
        delivery_tag=method.delivery_tag
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

    print("Waiting for click events...")

    channel.start_consuming()