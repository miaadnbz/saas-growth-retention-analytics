# Looker Studio Dashboard Build Guide

Build one report with four pages. Keep each page focused on one decision and place a one-sentence takeaway at the top.

## Page 1 — Executive Overview

**Audience:** VP Marketing, VP Product, Finance.

**Connect to:** `mart_channel_performance`, `fct_growth_funnel`, and `mart_cohort_retention`.

**Add:**

1. Scorecards: Signups, Activation Rate, Trial-to-Paid, 90-Day Retention, Paid Accounts, Realized Revenue.
2. Funnel: Signup → Activated → Paid → Retained at Day 90.
3. Bar chart: Revenue-to-Spend by channel.
4. Text box: “Activation is the largest controllable early growth lever.”
5. Recommendation box containing the three actions from `docs/executive_brief.md`.

**Executive takeaway to write:**

> Referral delivers the strongest customer economics, while Paid Social requires onboarding and targeting optimization. Growth planning should use retained CAC rather than signups or platform conversions alone.

## Page 2 — Acquisition & Unit Economics

**Connect to:** `mart_channel_performance`.

**Add:**

- Table by channel: Spend, Signups, Activation Rate, Paid Accounts, CAC, Retained CAC, Revenue, Revenue-to-Spend.
- Bubble chart: X = CAC, Y = 90-day retention, bubble size = paid accounts, dimension = channel.
- Monthly trend: Spend and paid conversions.
- Filters: Signup month, channel, country, company size, industry.

**Decision:** Protect or expand efficient channels; diagnose low-quality paid acquisition before increasing spend.

## Page 3 — Activation Funnel

**Connect to:** `fct_growth_funnel` and `mart_activation_drivers`.

**Add:**

- Funnel by critical onboarding action.
- Activation rate by channel and company size.
- Median days to activation.
- Table comparing 90-day retention for accounts that did and did not complete each milestone.

**Decision:** Choose the behavior and audience for the next onboarding experiment.

## Page 4 — Retention & Customer Health

**Connect to:** `mart_cohort_retention` and `mart_customer_health`.

**Add:**

- Cohort heatmap by signup month and months since conversion.
- Retention curves split by activated versus not activated.
- Health-score distribution.
- At-risk account table with account ID, MRR, last activity, support burden, and recommended action.

**Decision:** Prioritize high-value accounts for lifecycle or customer-success intervention.

## Publishing checklist

- Use a descriptive title: “SaaS Growth Analytics — Acquisition to Retention.”
- Add a “Methodology” text box with activation and retention definitions.
- Add a “Synthetic Data” badge on every page.
- Verify all percentages use average or ratio aggregation, not sum.
- Hide account-level pages from public sharing if you later replace synthetic data with real data.
- Add the public report link and three screenshots to the GitHub README.
