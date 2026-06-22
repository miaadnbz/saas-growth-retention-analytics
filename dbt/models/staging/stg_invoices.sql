select
    cast(invoice_id as string) as invoice_id,
    cast(account_id as string) as account_id,
    cast(invoice_date as date) as invoice_date,
    cast(amount as numeric) as amount,
    cast(payment_status as string) as payment_status
from {{ source('raw_saas', 'invoices') }}
