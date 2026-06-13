    
from django.db.models import F

from shortener.models import ShortURL
from config.redis import redis_client


from django.db import transaction
from django.utils import timezone

from analytics.models import ClickEvent
from config.redis import redis_client


def process_click(event: dict) -> None:

    short_code = event["short_code"]

    redis_key = f"clicks:{short_code}"
    redis_client.incr(redis_key)

    ClickEvent.objects.create(
        short_url=short_code,
        ip_address=event.get("ip_address"),
        user_agent=event.get("user_agent"),
        referrer=event.get("referrer"),
        created_at=timezone.now(),
    )

    
# TODO:Move flusher to shortener app
def flush_clicks():
    """
    Move Redis click counters into Postgres.
    """

    keys = redis_client.keys("clicks:*")

    for key in keys:

        count = redis_client.getdel(key)

        # if multiple workers call getdel, since getdel is atomic then all-1 get none from it.   
        if not count:
            continue

        short_code = key.split(":")[1]

        ShortURL.objects.filter(
            short_code=short_code
        ).update(
            click_count=F("click_count") + int(count)
        )