select
    a.account_id,
    count(t.ticket_id) as ticket_count,
    countif(t.priority = 'high') as high_priority_ticket_count,
    avg(t.resolution_hours) as avg_resolution_hours,
    avg(t.csat_score) as avg_csat
from {{ ref('stg_accounts') }} a
left join {{ ref('stg_support_tickets') }} t using (account_id)
group by 1
