select
  channel,
  spend,
  signups,
  activation_rate,
  paid_accounts,
  retention_90d_rate,
  cac,
  retained_cac,
  realized_revenue,
  revenue_to_spend,
  case
    when revenue_to_spend >= 2 and retention_90d_rate >= 0.70 then 'Protect and scale carefully'
    when activation_rate < 0.45 then 'Fix targeting or onboarding'
    when retained_cac is null then 'Measure incrementality before investment'
    else 'Maintain and test'
  end as recommended_decision
from `YOUR_GCP_PROJECT.analytics_saas.mart_channel_performance`
order by revenue_to_spend desc;
