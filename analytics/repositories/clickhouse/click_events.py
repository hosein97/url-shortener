from config.clickhouse import client


def insert_click_event(
    *,
    owner_id,
    short_code,
    original_url,
    ip_address,
    user_agent,
    referrer,
    created_at,
):
    client.insert(
        "click_events",
        [[
            owner_id,
            short_code,
            original_url,
            created_at,
            ip_address or "",
            user_agent or "",
            referrer or "",
        ]],
        column_names=[
            "owner_id",
            "short_code",
            "original_url",
            "created_at",
            "ip_address",
            "user_agent",
            "referrer",
        ],
    )


def get_dashboard(
    *,
    owner_id,
):
    result = client.query(
        """
        SELECT
            count() AS total_clicks,
            countIf(toDate(created_at) = today()) AS clicks_today,
            countIf(created_at >= now() - INTERVAL 7 DAY) AS clicks_last_7_days,
            uniq(ip_address) AS unique_visitors
        FROM click_events
        WHERE owner_id = {owner_id:Nullable(UInt64)}
        """,
        parameters={
            "owner_id": owner_id,
        },
    )

    row = result.first_row

    return {
        "total_clicks": row[0],
        "clicks_today": row[1],
        "clicks_last_7_days": row[2],
        "unique_visitors": row[3],
    }


def get_click_timeseries(
    *,
    owner_id,
    days,
):
    result = client.query(
        """
        SELECT
            toDate(created_at) AS date,
            count() AS clicks
        FROM click_events
        WHERE owner_id = {owner_id:Nullable(UInt64)}
          AND created_at >= now() - INTERVAL {days:UInt32} DAY
        GROUP BY date
        ORDER BY date
        """,
        parameters={
            "owner_id": owner_id,
            "days": days,
        },
    )

    return [
        {
            "date": row[0],
            "clicks": row[1],
        }
        for row in result.result_rows
    ]


def get_top_links(
    *,
    owner_id,
):
    result = client.query(
        """
        SELECT
            short_code,
            original_url,
            count() AS clicks,
            max(created_at) AS last_click
        FROM click_events
        WHERE owner_id = {owner_id:Nullable(UInt64)}
        GROUP BY
            short_code,
            original_url
        ORDER BY clicks DESC
        LIMIT 10
        """,
        parameters={
            "owner_id": owner_id,
        },
    )

    return [
        {
            "short_code": row[0],
            "original_url": row[1],
            "clicks": row[2],
            "last_click": row[3],
        }
        for row in result.result_rows
    ]


def get_link_stats(
    *,
    owner_id,
    short_codes,
):
    if not short_codes:
        return {}

    result = client.query(
        """
        SELECT
            short_code,
            any(original_url) AS original_url,
            count() AS clicks,
            max(created_at) AS last_click,
            uniq(ip_address) AS unique_visitors
        FROM click_events
        WHERE owner_id = {owner_id:Nullable(UInt64)}
          AND short_code IN {codes:Array(String)}
        GROUP BY short_code
        """,
        parameters={
            "owner_id": owner_id,
            "codes": short_codes,
        },
    )

    return {
        row[0]: {
            "original_url": row[1],
            "clicks": row[2],
            "last_click": row[3],
            "unique_visitors": row[4],
        }
        for row in result.result_rows
    }