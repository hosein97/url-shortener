from datetime import timedelta
from django.utils import timezone

from django.db.models import F

from config.redis import redis_client

from django.db import transaction
from django.utils import timezone

from analytics.models import ClickEvent
from shortener.models import ShortURL


def process_click(event: dict) -> None:

    short_code = event["short_code"]

    ClickEvent.objects.create(
        short_code=short_code,
        ip_address=event.get("ip_address"),
        user_agent=event.get("user_agent"),
        referrer=event.get("referrer"),
        created_at=timezone.now(),
    )

 

def get_dashboard_stats(*, user):
    """
    Return dashboard statistics.
    """

    if user.is_superuser:

        links = ShortURL.objects.all()

    else:

        links = ShortURL.objects.filter(
            owner=user
        )

    short_codes = list(
        links.values_list(
            "short_code",
            flat=True,
        )
    )

    recent_since = (
        timezone.now()
        - timedelta(days=1)
    )

    return {
        "total_links": links.count(),

        "total_clicks": ClickEvent.objects.filter(
            short_code__in=short_codes
        ).count(),

        "recent_clicks": ClickEvent.objects.filter(
            short_code__in=short_codes,
            created_at__gte=recent_since,
        ).count(),
    }