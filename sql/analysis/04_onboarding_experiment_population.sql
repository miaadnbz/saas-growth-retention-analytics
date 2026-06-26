select
  account_id,
  first_touch_channel,
  company_size,
  created_project_14d,
  invited_teammate_14d,
  connected_integration_14d
from `saas-growth-portfolio.analytics_saas_marts.mart_activation_drivers`
where first_touch_channel in ('Paid Social', 'Paid Search')
  and not is_activated_14d;
