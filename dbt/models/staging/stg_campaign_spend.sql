select
    cast(spend_month as date) as spend_month,
    cast(channel as string) as channel,
    cast(campaign_id as string) as campaign_id,
    cast(spend as numeric) as spend
from {{ source('raw_saas', 'campaign_spend') }}
