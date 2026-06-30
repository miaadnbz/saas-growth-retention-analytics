with paid as (

    select
        account_id,
        date_trunc(conversion_date, month) as conversion_cohort,
        conversion_date,
        cancel_date
    from {{ ref('int_account_retention') }}
    where is_paid

),

month_numbers as (

    select month_number
    from unnest(generate_array(0, 12)) as month_number

),

paid_with_observable_age as (

    select
        *,
        date_diff(
            date_trunc(
                date('{{ var("observation_end") }}'),
                month
            ),
            conversion_cohort,
            month
        ) as observable_months
    from paid

)

select
    p.conversion_cohort,
    m.month_number,
    count(*) as cohort_accounts,

    countif(
        p.cancel_date is null
        or p.cancel_date > date_add(
            p.conversion_date,
            interval m.month_number month
        )
    ) as retained_accounts,

    safe_divide(
        countif(
            p.cancel_date is null
            or p.cancel_date > date_add(
                p.conversion_date,
                interval m.month_number month
            )
        ),
        count(*)
    ) as retention_rate

from paid_with_observable_age p
cross join month_numbers m

-- Exclude cohort-month combinations that have not happened yet.
where m.month_number <= p.observable_months

group by
    p.conversion_cohort,
    m.month_number

order by
    p.conversion_cohort,
    m.month_number