select
    a.account_id,
    a.signup_date,
    date_trunc(a.signup_date, month) as signup_month,
    a.country,
    a.industry,
    a.company_size,
    a.first_touch_channel,
    a.first_touch_campaign_id,
    act.critical_actions_14d,
    act.is_activated_14d,
    r.is_paid,
    r.is_retained_90d,
    r.plan_name,
    r.monthly_recurring_revenue,
    rev.realized_revenue
from {{ ref('stg_accounts') }} a
left join {{ ref('int_account_activation') }} act using (account_id)
left join {{ ref('int_account_retention') }} r using (account_id)
left join {{ ref('int_account_revenue') }} rev using (account_id)
