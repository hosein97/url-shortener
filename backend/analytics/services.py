from analytics.repositories.postgres.link_ownership import (
    count_links,
    get_links_page,
)

from analytics.repositories.clickhouse.click_events import (
    get_dashboard,
    get_click_timeseries,
    get_top_links,
    get_link_stats,
)


def dashboard(
    *,
    owner_id,
):
    stats = get_dashboard(
        owner_id=owner_id,
    )

    return {
        "total_links": count_links(
            owner_id=owner_id,
        ),
        "total_clicks": stats["total_clicks"],
        "clicks_today": stats["clicks_today"],
        "clicks_last_7_days": stats["clicks_last_7_days"],
        "unique_visitors": stats["unique_visitors"],
    }


def top_links(
    *,
    owner_id,
):
    return get_top_links(
        owner_id=owner_id,
    )


def click_timeseries(
    *,
    owner_id,
    days,
):
    return get_click_timeseries(
        owner_id=owner_id,
        days=days,
    )


def links_dashboard(
    *,
    owner_id,
    page,
    page_size,
):
    offset = (page - 1) * page_size

    links = get_links_page(
        owner_id=owner_id,
        offset=offset,
        limit=page_size,
    )

    stats = get_link_stats(
        owner_id=owner_id,
        short_codes=[
            link.short_code
            for link in links
        ],
    )

    response = []

    for link in links:

        stat = stats.get(
            link.short_code,
            {},
        )

        response.append(
            {
                "short_code": link.short_code,
                "created_at": link.created_at,
                "original_url": stat.get("original_url"),
                "clicks": stat.get("clicks", 0),
                "unique_visitors": stat.get(
                    "unique_visitors",
                    0,
                ),
                "last_click": stat.get(
                    "last_click",
                ),
            }
        )

    return response