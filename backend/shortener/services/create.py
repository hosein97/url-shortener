import random
import string

from shortener.models import ShortURL


def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits

    return ''.join(
        random.choices(characters, k=length)
    )


def create_short_url(
    *,
    original_url,
    owner=None,
):

    short_code = generate_short_code()

    while ShortURL.objects.filter(
        short_code=short_code
    ).exists():

        short_code = generate_short_code()

    short_url = ShortURL.objects.create(
        owner=owner,
        original_url=original_url,
        short_code=short_code,
    )

    return short_url
