import random
import string
import logging
import time 

from django.db.models import F

from .models import ShortURL
from config.redis import redis_client

logger = logging.getLogger(__name__)

def increment_clicks(short_code: str):

    try:
        redis_client.incr(
            f"clicks:{short_code}"
        )
    except redis.RedisError:
        logger.exception(
            "Redis INC failed"
        )
def get_original_url(short_code: str) -> str:
    
    start = time.perf_counter()

    cache_key = f"url:{short_code}"
    
    try:
        
        cached_url = redis_client.get(cache_key)
        
        if cached_url:
            logger.info(
                f"Cache HIT for {short_code}"
            )

            elapsed = time.perf_counter() - start

            logger.info(
                f"Cache HIT took {elapsed:.6f}s"
            )
            return cached_url

        logger.info(
            f"Cache MISS for {short_code}"
        )   
    except redis.RedisError:
        logger.exception(
            "Redis GET failed"
        )

    short_url = ShortURL.objects.get(
        short_code=short_code
    )
    
    try:
        redis_client.set(
            cache_key,
            short_url.original_url,
            ex=3600
        )
    except redis.RedisError:
        logger.exception(
            "Redis SET failed"
        )

    elapsed = time.perf_counter() - start

    logger.info(
        f"DB lookup took {elapsed:.6f}s"
    )
        
    return short_url.original_url


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