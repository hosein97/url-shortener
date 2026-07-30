CREATE TABLE IF NOT EXISTS analytics.click_events
(
    owner_id UInt64,

    short_code String,

    original_url String,

    created_at DateTime,

    ip_address String,

    user_agent String,

    referrer String
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(created_at)
ORDER BY (
    owner_id,
    short_code,
    created_at
);