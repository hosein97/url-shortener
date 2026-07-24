import pika
import json

from decouple import config


def get_connection():
    credentials = pika.PlainCredentials(
        config("RABBITMQ_USER"),
        config("RABBITMQ_PASSWORD"),
    )

    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host=config("RABBITMQ_HOST"),
            port=config("RABBITMQ_PORT", cast=int),
            credentials=credentials,
        )
    )
    
    
def publish_click(event):

    connection = get_connection()
    channel = connection.channel()

    channel.exchange_declare(
        exchange="clicks",
        exchange_type="fanout",
        durable=True,
    )

    channel.basic_publish(
        exchange="clicks",
        routing_key="",
        body=json.dumps(event),
    )

    connection.close()