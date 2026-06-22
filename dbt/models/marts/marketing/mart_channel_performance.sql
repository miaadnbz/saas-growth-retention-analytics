with outcomes as (
    select
        first_touch_channel as channel,
        count(*) as signups,
        countif(is_activated_14d) as activated_accounts,
        countif(is_paid) as paid_accounts,
        countif(is_retained_90d) as retained_90d_accounts,
        sum(realized_revenue) as realized_revenue
    from {{ ref('fct_growth_funnel') }}
    group by 1
), spend as (
    select channel, sum(spend) as spend
    from {{ ref('stg_campaign_spend') }}
    group by 1
)
select
    o.channel,
    o.signups,
    o.activated_accounts,
    safe_divide(o.activated_accounts, o.signups) as activation_rate,
    o.paid_accounts,
    safe_divide(o.paid_accounts, o.signups) as trial_to_paid_rate,
    o.retained_90d_accounts,
    safe_divide(o.retained_90d_accounts, o.paid_accounts) as retention_90d_rate,
    coalesce(s.spend, 0) as spend,
    safe_divide(s.spend, o.paid_accounts) as cac,
    safe_divide(s.spend, o.retained_90d_accounts) as retained_cac,
    o.realized_revenue,
    safe_divide(o.realized_revenue, s.spend) as revenue_to_spend
from outcomes o
left join spend s using (channel)
