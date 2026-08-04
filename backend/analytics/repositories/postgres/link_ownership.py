from analytics.models import LinkOwnership


def register_link(
    *,
    short_code,
    original_url,
    owner_id,
    created_at,
):
    LinkOwnership.objects.create(
        short_code=short_code,
        original_url=original_url,
        owner_id=owner_id,
        created_at=created_at,
    )

def count_links(
    *,
    owner_id,
):
    return (
        LinkOwnership.objects
        .filter(owner_id=owner_id)
        .count()
    )


def get_by_short_code(short_code: str) -> LinkOwnership:

    return LinkOwnership.objects.only(
        "owner_id",
        "short_code",
        "original_url",
    ).get(
        short_code=short_code,
    )
    
    
    
def get_links_page(
    *,
    owner_id,
    offset,
    limit,
):
    return list(
        LinkOwnership.objects.filter(
            owner_id=owner_id,
        )
        .order_by("-created_at")[offset:offset + limit]
    )