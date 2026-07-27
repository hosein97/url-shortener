from datetime import timedelta
from django.utils import timezone

from django.db.models import F

from config.redis import redis_client

from django.db import transaction
from django.db.models import Count, Max
from django.db.models.functions import TruncDate

from analytics.models import ClickEvent, LinkOwnership



def process_click(event: dict) -> None:

    short_code = event["short_code"]

    ClickEvent.objects.create(
        short_code=short_code,
        ip_address=event.get("ip_address"),
        user_agent=event.get("user_agent"),
        referrer=event.get("referrer"),
        created_at=timezone.now(),
    )

 


def get_click_timeseries(
    *,
    owner_id: int,
    days: int,
):

    short_codes = (
        LinkOwnership.objects
        .filter(
            owner_id=owner_id,
        )
        .values_list(
            "short_code",
            flat=True,
        )
    )

    start_date = (
        timezone.now()
        - timedelta(days=days)
    )

    return (
        ClickEvent.objects
        .filter(
            short_code__in=short_codes,
            created_at__gte=start_date,
        )
        .annotate(
            date=TruncDate("created_at"),
        )
        .values("date")
        .annotate(
            clicks=Count("id"),
        )
        .order_by("date")
    )



def get_dashboard(
    *,
    owner_id: int,
):

    short_codes = list(
        LinkOwnership.objects.filter(
            owner_id=owner_id,
        ).values_list(
            "short_code",
            flat=True,
        )
    )

    now = timezone.now()

    today = now.date()

    last_7_days = now - timedelta(days=7)

    return {
        "total_links": len(short_codes),

        "total_clicks": ClickEvent.objects.filter(
            short_code__in=short_codes,
        ).count(),

        "clicks_today": ClickEvent.objects.filter(
            short_code__in=short_codes,
            created_at__date=today,
        ).count(),

        "clicks_last_7_days": ClickEvent.objects.filter(
            short_code__in=short_codes,
            created_at__gte=last_7_days,
        ).count(),
    }






def get_top_links(
    *,
    owner_id: int,
):

    short_codes = (
        LinkOwnership.objects
        .filter(
            owner_id=owner_id,
        )
        .values_list(
            "short_code",
            flat=True,
        )
    )

    return (
        ClickEvent.objects
        .filter(
            short_code__in=short_codes,
        )
        .values(
            "short_code",
        )
        .annotate(
            clicks=Count("id"),
            last_click=Max("created_at"),
        )
        .order_by("-clicks")
    )


#TODO: dont call this directly from shortner, rabbitmq consumer should call this instead
def register_link(
    *,
    short_code,
    owner_id,
    created_at,
):
    LinkOwnership.objects.create(
        short_code=short_code,
        owner_id=owner_id,
        created_at=created_at,
    )