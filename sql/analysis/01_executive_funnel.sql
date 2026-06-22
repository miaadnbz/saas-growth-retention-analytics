select
  count(*) as signups,
  countif(is_activated_14d) as activated,
  countif(is_paid) as paid,
  countif(is_retained_90d) as retained_90d,
  safe_divide(countif(is_activated_14d), count(*)) as activation_rate,
  safe_divide(countif(is_paid), count(*)) as trial_to_paid_rate,
  safe_divide(countif(is_retained_90d), countif(is_paid)) as retention_90d_rate
from `YOUR_GCP_PROJECT.analytics_saas.fct_growth_funnel`;
