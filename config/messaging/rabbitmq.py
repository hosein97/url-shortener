import pika

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
    
def publish_click(event: dict):

    connection = get_connection()

    channel = connection.channel()

    channel.queue_declare(
        queue="clicks",
        durable=True,
    )

    channel.basic_publish(
        exchange="",
        routing_key="clicks",
        body=json.dumps(event),
    )

    connection.close()