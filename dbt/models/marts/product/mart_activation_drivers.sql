with events as (
    select
        a.account_id,
        countif(e.event_name = 'created_project' and date(e.event_timestamp) <= date_add(a.signup_date, interval 13 day)) > 0 as created_project_14d,
        countif(e.event_name = 'invited_teammate' and date(e.event_timestamp) <= date_add(a.signup_date, interval 13 day)) > 0 as invited_teammate_14d,
        countif(e.event_name = 'connected_integration' and date(e.event_timestamp) <= date_add(a.signup_date, interval 13 day)) > 0 as connected_integration_14d
    from {{ ref('stg_accounts') }} a
    left join {{ ref('stg_product_events') }} e using (account_id)
    group by 1
)
select
    f.account_id,
    f.first_touch_channel,
    f.company_size,
    e.created_project_14d,
    e.invited_teammate_14d,
    e.connected_integration_14d,
    f.is_activated_14d,
    f.is_paid,
    f.is_retained_90d,
    f.realized_revenue
from {{ ref('fct_growth_funnel') }} f
join events e using (account_id)
