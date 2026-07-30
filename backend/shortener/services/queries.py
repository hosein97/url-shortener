from django.shortcuts import get_object_or_404

from shortener.models import ShortURL

def get_user_links(
    *,
    user,
):
    return (
        ShortURL.objects
        .filter(owner=user)
        .order_by("-created_at")
    )
    
    
    
def get_short_url(
    *,
    short_url_id,
    owner,
):
    return get_object_or_404(
        ShortURL,
        pk=short_url_id,
        owner=owner,
    )