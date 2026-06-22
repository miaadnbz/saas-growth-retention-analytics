select
    cast(ticket_id as string) as ticket_id,
    cast(account_id as string) as account_id,
    cast(created_at as timestamp) as created_at,
    cast(priority as string) as priority,
    cast(resolution_hours as numeric) as resolution_hours,
    cast(csat_score as numeric) as csat_score
from {{ source('raw_saas', 'support_tickets') }}
