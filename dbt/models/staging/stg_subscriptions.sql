select
    cast(subscription_id as string) as subscription_id,
    cast(account_id as string) as account_id,
    cast(trial_start_date as date) as trial_start_date,
    cast(conversion_date as date) as conversion_date,
    cast(plan_name as string) as plan_name,
    cast(monthly_recurring_revenue as numeric) as monthly_recurring_revenue,
    cast(cancel_date as date) as cancel_date,
    cast(status as string) as status
from {{ source('raw_saas', 'subscriptions') }}
