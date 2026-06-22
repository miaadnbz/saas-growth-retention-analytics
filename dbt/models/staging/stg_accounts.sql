select
    cast(account_id as string) as account_id,
    cast(signup_date as date) as signup_date,
    cast(country as string) as country,
    cast(industry as string) as industry,
    cast(company_size as string) as company_size,
    cast(first_touch_channel as string) as first_touch_channel,
    cast(first_touch_campaign_id as string) as first_touch_campaign_id,
    cast(trial_days as int64) as trial_days
from {{ source('raw_saas', 'accounts') }}
