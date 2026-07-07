# Looker Studio Dashboard Specification

## Overview

**Report title:** SaaS Growth Analytics — Acquisition to Retention
**Platform:** Looker Studio
**Data warehouse:** BigQuery
**Transformation layer:** dbt
**Data classification:** 100% synthetic portfolio data

The dashboard connects marketing acquisition, onboarding behaviour, subscription conversion, realized revenue, customer retention, support activity, and customer-health indicators.

It is designed to help Marketing, Product, Finance, and Customer Success evaluate growth using downstream customer quality rather than signup volume or platform-reported conversions alone.

## Primary business question

**Which acquisition channels bring customers who activate, convert, and remain subscribed—and where should Marketing and Product invest next?**

## Report structure

The report contains five pages:

1. Executive Overview
2. Acquisition & Unit Economics
3. Activation Drivers
4. Retention & Cohorts
5. Customer Health

---

## Page 1: Executive Overview

### Audience

* VP Marketing
* VP Product
* Finance leadership
* Growth leadership

### Purpose

Provide a concise view of lifecycle performance, channel economics, funnel progression, and the highest-priority business action.

### Primary data sources

* `mart_channel_performance`
* `fct_growth_funnel`

### Key metrics

* Trial signups
* 14-day activation rate
* Trial-to-paid conversion rate
* 90-day paid retention
* Realized invoice revenue
* Activated, paid, and retained account counts

### Visuals

* Lifecycle KPI scorecards
* Signup-to-retention funnel
* Realized revenue per dollar of attributed marketing spend
* Executive recommendation panel
* Quantified Paid Social activation scenario

### Decision supported

Determine where leadership should protect efficient acquisition, where optimization is required, and which onboarding intervention should be tested next.

### Executive interpretation

Referral and Organic Search show the strongest observed revenue efficiency. Paid Social has the weakest activation and revenue-to-spend performance, making it the clearest paid-channel optimization opportunity.

A day-3 onboarding intervention should be tested before additional Paid Social budget is committed.

---

## Page 2: Acquisition & Unit Economics

### Audience

* Growth Marketing
* Performance Marketing
* Finance
* Marketing Analytics

### Purpose

Compare acquisition channels using customer quality and downstream economics rather than signup volume alone.

### Primary data source

* `mart_channel_performance`

### Key metrics

* Marketing spend
* Trial signups
* Activation rate
* Paid accounts
* Customer acquisition cost
* Retained customer acquisition cost
* 90-day retained accounts
* Realized revenue
* Revenue-to-spend ratio

### Visuals

* Channel performance table
* CAC versus 90-day retention bubble chart
* Channel selector
* Unit-economics interpretation panel

### Decision supported

Identify channels to protect, optimize, test, or reduce based on acquisition cost, retained-customer quality, and realized revenue.

### Interpretation guidance

Direct traffic is excluded from paid-channel efficiency comparisons when attributed marketing spend is zero.

Revenue-to-spend is observational and should not be interpreted as incremental profitability or causal return on advertising spend.

---

## Page 3: Activation Drivers

### Audience

* Product
* Growth
* Lifecycle Marketing
* Customer Onboarding

### Purpose

Identify the acquisition sources and customer characteristics associated with stronger 14-day activation.

### Primary data source

* `mart_activation_drivers`

### Activation definition

An account is activated when it completes at least two of the following actions within 14 days of signup:

* Create a project
* Invite a teammate
* Connect an integration

### Key metrics

* Overall 14-day activation rate
* Activation rate by acquisition channel
* Activation rate by company size
* Onboarding milestone completion by channel

### Visuals

* Overall activation scorecard
* Activation by acquisition channel
* Activation by company size
* Onboarding milestone completion heatmap
* Activation insight and experiment recommendation

### Decision supported

Select the customer segment and onboarding behaviour to target in the next growth experiment.

### Executive interpretation

Paid Social has the lowest observed activation rate and the weakest teammate-invitation and integration-connection completion rates.

The recommended experiment targets under-activated Paid Social trials with a day-3 onboarding intervention.

---

## Page 4: Retention & Cohorts

### Audience

* Product
* Customer Analytics
* Growth
* Finance

### Purpose

Show how customer retention changes over the paid lifecycle and assess the relationship between early activation and 90-day retention.

### Primary data sources

* `mart_cohort_retention`
* `fct_growth_funnel`

### Key metrics

* Monthly cohort retention
* 90-day retention by activation status
* Retention difference between activated and non-activated paid accounts

### Visuals

* 12-month cohort-retention heatmap
* Recent cohort-retention curves
* Activated versus non-activated 90-day retention comparison
* Retention insight panel
* Cohort-date control

### Decision supported

Determine when customer loss is concentrated and whether early onboarding should be prioritized as a retention intervention.

### Executive interpretation

Customer loss is concentrated in the first three paid months.

Activated paid accounts show materially higher 90-day retention than non-activated paid accounts. This is an observational association and should be validated through experimentation.

---

## Page 5: Customer Health

### Audience

* Customer Success
* Account Management
* Customer Analytics
* Revenue Operations

### Purpose

Identify paid accounts requiring intervention and prioritize them according to engagement, support risk, and monthly recurring revenue.

### Primary data source

* `mart_customer_health`

### Key metrics

* At-risk paid accounts
* Share of paid accounts at risk
* Monthly recurring revenue associated with at-risk accounts
* Accounts with no activity in the previous 30 days
* Accounts with high-priority support tickets
* Customer health score

### Visuals

* Customer-health scorecards
* At-risk account intervention table
* Numeric health-score distribution
* Customer-success priority panel

### Decision supported

Prioritize customer-success outreach toward high-value accounts with low health scores, limited recent activity, or unresolved support risk.

### Interpretation guidance

MRR at risk represents revenue associated with flagged accounts. It is not a forecast that all identified revenue will churn.

The customer-health score is a transparent business rule designed for prioritization. It is not a statistically calibrated probability of churn.

---

## Metric governance

All percentages and rates use ratio or average aggregation rather than summation.

The principal governed metrics are:

* 14-day activation rate
* Trial-to-paid conversion rate
* 90-day paid retention
* CAC
* Retained CAC
* Realized revenue
* Revenue-to-spend
* Customer health score

Metric definitions are documented in the repository README and dbt model documentation.

## Data-quality controls

The dashboard is supported by dbt tests covering:

* Primary-key uniqueness
* Non-null identifiers
* Accepted categorical values
* Source-to-model relationships
* Logical subscription dates
* One row per account in customer marts
* Revenue reconciliation
* Cohort observation logic

## Design standards

* Freeform desktop layout
* Consistent report-level navigation
* Synthetic-data disclosure on every page
* Business-friendly field labels
* Minimal use of technical database names
* Percentages displayed as rates, not summed values
* Currency metrics displayed without unnecessary decimal precision
* Decision-oriented titles, annotations, and recommendation panels

## Analytical limitations

* The dataset is synthetic and intended for portfolio demonstration.
* First-touch attribution simplifies multi-touch acquisition journeys.
* Revenue-to-spend is observational and does not measure causal incrementality.
* Activation and retention relationships may reflect customer motivation or selection effects.
* The quantified Paid Social scenario is a planning estimate rather than a financial forecast.
* Recommended interventions should be validated through controlled experiments.
