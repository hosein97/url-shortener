import random
import string

from django.db.models import F

from .models import ShortURL

def increment_clicks(short_url_id: int):

    ShortURL.objects.filter(
        id=short_url_id
    ).update(
        clicks=F("clicks") + 1
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