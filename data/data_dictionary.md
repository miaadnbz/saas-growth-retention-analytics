# Data Dictionary

All data is synthetic and generated with a fixed random seed. No real customer, company, or personal data is included.

## `accounts`

| Field | Type | Description |
|---|---|---|
| `account_id` | `object` | Unique customer account identifier. |
| `signup_date` | `datetime64[ns]` | Date the trial account was created. |
| `country` | `object` | Customer country. |
| `industry` | `object` | Customer industry. |
| `company_size` | `object` | Employee-size band. |
| `first_touch_channel` | `object` | First recorded acquisition channel. |
| `first_touch_campaign_id` | `object` | First-touch campaign identifier. |
| `trial_days` | `int64` | Trial duration in days. |

## `marketing_touches`

| Field | Type | Description |
|---|---|---|
| `touch_id` | `object` | Unique marketing touch identifier. |
| `account_id` | `object` | Customer account identifier. |
| `touch_date` | `datetime64[ns]` | Date of marketing interaction. |
| `channel` | `object` | Marketing channel. |
| `campaign_id` | `object` | Campaign identifier. |
| `touch_position` | `int64` | Chronological position in the journey. |
| `touch_count` | `int64` | Total touches before signup. |

## `product_events`

| Field | Type | Description |
|---|---|---|
| `event_id` | `object` | Unique product event identifier. |
| `account_id` | `object` | Customer account identifier. |
| `event_timestamp` | `datetime64[ns]` | Event date/time. |
| `event_name` | `object` | Product behavior event. |

## `subscriptions`

| Field | Type | Description |
|---|---|---|
| `subscription_id` | `object` | Unique subscription identifier. |
| `account_id` | `object` | Customer account identifier. |
| `trial_start_date` | `datetime64[ns]` | Trial start date. |
| `conversion_date` | `datetime64[ns]` | Date trial became paid. |
| `plan_name` | `object` | Subscription plan. |
| `monthly_recurring_revenue` | `int64` | Monthly recurring revenue in CAD-equivalent synthetic dollars. |
| `cancel_date` | `datetime64[ns]` | Cancellation date, if applicable. |
| `status` | `object` | Current synthetic subscription status at observation end. |

## `invoices`

| Field | Type | Description |
|---|---|---|
| `invoice_id` | `object` | Unique invoice identifier. |
| `account_id` | `object` | Customer account identifier. |
| `invoice_date` | `datetime64[ns]` | Invoice date. |
| `amount` | `float64` | Paid invoice amount. |
| `payment_status` | `object` | Invoice payment status. |

## `support_tickets`

| Field | Type | Description |
|---|---|---|
| `ticket_id` | `object` | Unique ticket identifier. |
| `account_id` | `object` | Customer account identifier. |
| `created_at` | `datetime64[ns]` | Ticket creation date. |
| `priority` | `object` | Ticket priority. |
| `resolution_hours` | `float64` | Hours to resolution. |
| `csat_score` | `float64` | Customer satisfaction score from 1 to 5. |

## `campaign_spend`

| Field | Type | Description |
|---|---|---|
| `spend_month` | `datetime64[ns]` | Month of spend. |
| `channel` | `object` | Marketing channel. |
| `campaign_id` | `object` | Campaign identifier. |
| `spend` | `float64` | Monthly campaign spend. |
