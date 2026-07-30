from analytics.models import LinkOwnership


def register_link(
    *,
    short_code,
    owner_id,
    created_at,
):
    LinkOwnership.objects.create(
        short_code=short_code,
        owner_id=owner_id,
        created_at=created_at,
    )


def get_owner_short_codes(
    *,
    owner_id,
):
    return list(
        LinkOwnership.objects
        .filter(owner_id=owner_id)
        .values_list(
            "short_code",
            flat=True,
        )
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