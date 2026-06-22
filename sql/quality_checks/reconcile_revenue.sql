with invoice_total as (
  select sum(amount) as amount
  from `YOUR_GCP_PROJECT.staging.stg_invoices`
  where payment_status = 'paid'
), mart_total as (
  select sum(realized_revenue) as amount
  from `YOUR_GCP_PROJECT.analytics_saas.mart_channel_performance`
)
select
  invoice_total.amount as source_revenue,
  mart_total.amount as mart_revenue,
  invoice_total.amount - mart_total.amount as difference
from invoice_total cross join mart_total;
