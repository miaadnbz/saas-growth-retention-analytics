select
  is_activated_14d,
  count(*) as accounts,
  safe_divide(countif(is_paid), count(*)) as trial_to_paid_rate,
  safe_divide(countif(is_retained_90d), countif(is_paid)) as retention_90d_rate,
  avg(realized_revenue) as avg_realized_revenue_per_signup
from `YOUR_GCP_PROJECT.analytics_saas.fct_growth_funnel`
group by 1;
