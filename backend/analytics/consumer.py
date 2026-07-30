import logging
import json
import pika

from config.messaging.rabbitmq import get_connection

from django.utils import timezone


from analytics.repositories.postgres.link_ownership import (
    get_by_short_code,
)

from analytics.repositories.clickhouse.click_events import (
    insert_click_event,
)

logger = logging.getLogger(__name__)


def process_click(event: dict):

    link = get_by_short_code(
        event["short_code"]
    )

    insert_click_event(
        owner_id=link.owner_id if link.owner_id is not None else 0,
        short_code=link.short_code,
        original_url=link.original_url,

        ip_address=event.get("ip_address"),
        user_agent=event.get("user_agent"),
        referrer=event.get("referrer"),

        created_at=timezone.now(),
    )

    

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

    channel.exchange_declare(
    exchange="clicks",
    exchange_type="fanout",
    durable=True,
)

    channel.queue_declare(
        queue="analytics.clicks",
        durable=True,
    )

    channel.queue_bind(
        exchange="clicks",
        queue="analytics.clicks",
    )

    channel.basic_consume(
        queue="analytics.clicks",
        on_message_callback=callback,
    )

    logger.info("Waiting for click events...")

    channel.start_consuming()