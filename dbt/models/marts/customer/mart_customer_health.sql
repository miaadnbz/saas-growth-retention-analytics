with recent_events as (
    select
        account_id,
        max(date(event_timestamp)) as last_activity_date,
        countif(date(event_timestamp) >= date_sub(date('{{ var('observation_end') }}'), interval 30 day)) as events_last_30d
    from {{ ref('stg_product_events') }}
    group by 1
)
select
    f.account_id,
    f.first_touch_channel,
    f.company_size,
    f.plan_name,
    f.monthly_recurring_revenue,
    f.is_activated_14d,
    f.is_retained_90d,
    e.last_activity_date,
    e.events_last_30d,
    s.ticket_count,
    s.high_priority_ticket_count,
    s.avg_csat,
    40 * cast(f.is_activated_14d as int64)
      + 30 * cast(coalesce(e.events_last_30d, 0) >= 4 as int64)
      + 20 * cast(coalesce(s.high_priority_ticket_count, 0) = 0 as int64)
      + 10 * cast(coalesce(s.avg_csat, 5) >= 4 as int64) as health_score,
    case
      when not f.is_activated_14d then 'Onboarding intervention'
      when coalesce(e.events_last_30d, 0) < 4 and f.monthly_recurring_revenue >= 99 then 'Customer success outreach'
      when coalesce(s.high_priority_ticket_count, 0) > 0 then 'Resolve support risk'
      else 'Monitor'
    end as recommended_action
from {{ ref('fct_growth_funnel') }} f
left join recent_events e using (account_id)
left join {{ ref('int_account_support') }} s using (account_id)
where f.is_paid
