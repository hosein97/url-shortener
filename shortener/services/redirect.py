import time 
import redis 

from django.db.models import F
from django.shortcuts import get_object_or_404

from shortener.models import ShortURL
from config.redis import redis_client

import logging

logger = logging.getLogger(__name__)

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

    short_url = get_object_or_404(
        ShortURL,
        short_code=short_code,
    )
  
    elapsed = time.perf_counter() - start

    logger.info(
        f"DB lookup took {elapsed:.6f}s"
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
      
    return short_url.original_url
