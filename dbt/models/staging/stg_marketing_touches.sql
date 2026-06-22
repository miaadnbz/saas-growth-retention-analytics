select
    cast(touch_id as string) as touch_id,
    cast(account_id as string) as account_id,
    cast(touch_date as date) as touch_date,
    cast(channel as string) as channel,
    cast(campaign_id as string) as campaign_id,
    cast(touch_position as int64) as touch_position,
    cast(touch_count as int64) as touch_count
from {{ source('raw_saas', 'marketing_touches') }}
