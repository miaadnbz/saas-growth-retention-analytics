select
    conversion_cohort,
    month_number

from {{ ref('mart_cohort_retention') }}

where month_number > date_diff(
    date_trunc(
        date('{{ var("observation_end") }}'),
        month
    ),
    conversion_cohort,
    month
)