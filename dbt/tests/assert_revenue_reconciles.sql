-- This test passes when paid invoice revenue and channel-mart
-- realized revenue differ by no more than one cent.

with invoice_total as (

    select
        coalesce(sum(amount), 0) as source_revenue

    from {{ ref('stg_invoices') }}

    where payment_status = 'paid'

),

mart_total as (

    select
        coalesce(sum(realized_revenue), 0) as mart_revenue

    from {{ ref('mart_channel_performance') }}

),

reconciliation as (

    select
        source_revenue,
        mart_revenue,
        source_revenue - mart_revenue as difference

    from invoice_total
    cross join mart_total

)

select
    source_revenue,
    mart_revenue,
    difference

from reconciliation

where abs(difference) > 0.01