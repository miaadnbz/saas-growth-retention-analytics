select
    a.account_id,
    coalesce(sum(i.amount), 0) as realized_revenue,
    count(i.invoice_id) as paid_invoice_count,
    max(i.invoice_date) as latest_invoice_date
from {{ ref('stg_accounts') }} a
left join {{ ref('stg_invoices') }} i
  on a.account_id = i.account_id
 and i.payment_status = 'paid'
group by 1
