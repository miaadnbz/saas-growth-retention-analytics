select
    cast(event_id as string) as event_id,
    cast(account_id as string) as account_id,
    cast(event_timestamp as timestamp) as event_timestamp,
    cast(event_name as string) as event_name
from {{ source('raw_saas', 'product_events') }}
