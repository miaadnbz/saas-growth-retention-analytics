with critical_events as (
    select
        a.account_id,
        a.signup_date,
        min(if(e.event_name = 'created_project', date(e.event_timestamp), null)) as created_project_date,
        min(if(e.event_name = 'invited_teammate', date(e.event_timestamp), null)) as invited_teammate_date,
        min(if(e.event_name = 'connected_integration', date(e.event_timestamp), null)) as connected_integration_date
    from {{ ref('stg_accounts') }} a
    left join {{ ref('stg_product_events') }} e using (account_id)
    group by 1, 2
), scored as (
    select
        *,
        if(created_project_date between signup_date and date_add(signup_date, interval 13 day), 1, 0)
        + if(invited_teammate_date between signup_date and date_add(signup_date, interval 13 day), 1, 0)
        + if(connected_integration_date between signup_date and date_add(signup_date, interval 13 day), 1, 0)
          as critical_actions_14d
    from critical_events
)
select
    *,
    critical_actions_14d >= 2 as is_activated_14d,
    (select min(action_date) from unnest([created_project_date, invited_teammate_date, connected_integration_date]) as action_date) as first_critical_action_date
from scored
