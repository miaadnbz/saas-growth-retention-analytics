-- Diagnostic version of the automated dbt revenue reconciliation test.
-- Use this query to inspect the source total, mart total, and difference.

with invoice_total as (
  select sum(amount) as amount
  from `saas-growth-portfolio.analytics_saas_staging.stg_invoices`
  where payment_status = 'paid'
), mart_total as (
  select sum(realized_revenue) as amount
  from `saas-growth-portfolio.analytics_saas_marts.mart_channel_performance`
)
select
  invoice_total.amount as source_revenue,
  mart_total.amount as mart_revenue,
  invoice_total.amount - mart_total.amount as difference
from invoice_total cross join mart_total;
