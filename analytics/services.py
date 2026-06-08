    
from django.db.models import F

from shortener.models import ShortURL
from config.redis import redis_client


def process_click(short_code: str) -> None:

    key = f"clicks:{short_code}"

    redis_client.incr(key)
    
    
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