select
    s.account_id,
    s.conversion_date,
    s.cancel_date,
    s.monthly_recurring_revenue,
    s.plan_name,
    s.conversion_date is not null as is_paid,
    case
      when s.conversion_date is null then null
      when date('{{ var('observation_end') }}') < date_add(s.conversion_date, interval 90 day) then null
      else s.cancel_date is null or s.cancel_date > date_add(s.conversion_date, interval 90 day)
    end as is_retained_90d,
    case
      when s.conversion_date is null then null
      when s.cancel_date is null then date_diff(date('{{ var('observation_end') }}'), s.conversion_date, day)
      else date_diff(s.cancel_date, s.conversion_date, day)
    end as paid_tenure_days
from {{ ref('stg_subscriptions') }} s
