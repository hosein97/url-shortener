from django.db.models import F

from config.redis import redis_client

from django.db import transaction
from django.utils import timezone

from analytics.models import ClickEvent


def process_click(event: dict) -> None:

    short_code = event["short_code"]

    ClickEvent.objects.create(
        short_code=short_code,
        ip_address=event.get("ip_address"),
        user_agent=event.get("user_agent"),
        referrer=event.get("referrer"),
        created_at=timezone.now(),
    )

    
