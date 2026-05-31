import random
import string

from django.db.models import F

from .models import ShortURL
from .redis_client import redis_client

def increment_clicks(short_code: str):

    redis_client.incr(
        f"clicks:{short_code}"
    )

def flush_clicks():
    for key in redis_client.scan_iter("clicks:*"):

        count = redis_client.getdel(key)

        # if multiple workers call getdel, since getdel is atomic then all-1 get none from it.   
        if not count:
            continue

        short_code = key.replace("clicks:", "")

        ShortURL.objects.filter(
            short_code=short_code
        ).update(
            clicks=F("clicks") + int(count)
        )
    
def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits

    return ''.join(
        random.choices(characters, k=length)
    )


def create_short_url(original_url):

    short_code = generate_short_code()

    while ShortURL.objects.filter(
        short_code=short_code
    ).exists():

        short_code = generate_short_code()

    short_url = ShortURL.objects.create(
        original_url=original_url,
        short_code=short_code
    )

    return short_url