import logging
import redis

from django.http import JsonResponse
from django.urls import resolve, Resolver404
from django.conf import settings
from config.redis import redis_client

logger = logging.getLogger(__name__)


class RateLimitMiddleware:

    LIMIT = 100
    WINDOW_SECONDS = 60

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if settings.DEBUG:
            return self.get_response(request)

        try:
            match = resolve(request.path)
        except Resolver404:
            return self.get_response(request)

        if match.view_name != "redirect":
            return self.get_response(request)

        ip = request.META.get("REMOTE_ADDR", "unknown")

        try:
            key = f"rate_limit:{ip}"

            count = redis_client.incr(key)

            if count == 1:
                redis_client.expire(
                    key,
                    self.WINDOW_SECONDS,
                )

            if count > self.LIMIT:

                response = JsonResponse(
                    {"detail": "Rate limit exceeded"},
                    status=429,
                )

                response["Retry-After"] = str(
                    self.WINDOW_SECONDS
                )

                return response

        except redis.RedisError:
            logger.exception(
                "Redis error during rate limiting"
            )

        return self.get_response(request)