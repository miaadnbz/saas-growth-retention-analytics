# Build and Publish This Portfolio Project

This guide assumes Windows, VS Code, GitHub, BigQuery, dbt Core, and Looker Studio.

## 1. Understand the case before touching the code

The business is a fictional B2B SaaS company. It has growing trial volume but cannot tell which channels produce customers who activate, pay, and retain.

**Executive question:** Which acquisition channels bring customers who activate, convert, and remain subscribed—and where should Marketing and Product invest next?

**Decision to support:** Allocate next-quarter marketing and onboarding resources toward retained subscription revenue rather than trial volume.

**Audience:** VP Marketing, VP Product, Finance, and Customer Success.

The project is deliberately structured as a decision case:

- Situation: trial registrations are growing.
- Complication: marketing, product, billing, and support data are disconnected.
- Question: which channels and onboarding behaviours create durable revenue?
- Answer: connect customer-level data, measure downstream quality, and test an activation intervention.

## 2. Open the project locally

1. Extract the downloaded ZIP.
2. Open VS Code.
3. Select **File → Open Folder**.
4. Choose the `saas-growth-analytics` folder.
5. Open **Terminal → New Terminal**.

Run in PowerShell:

```powershell
py -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/generate_synthetic_data.py
```

The generator creates seven synthetic source tables in `data/raw/`:

- `accounts.csv`
- `marketing_touches.csv`
- `product_events.csv`
- `subscriptions.csv`
- `invoices.csv`
- `support_tickets.csv`
- `campaign_spend.csv`

Do not describe this as real company data. State clearly that it is a reproducible synthetic case study.

## 3. Create the GitHub repository

Create a public repository named:

```text
saas-growth-retention-analytics
```

Use this description:

```text
End-to-end SaaS growth analytics case study connecting acquisition, product activation, subscription revenue, and 90-day retention using SQL, dbt, BigQuery, Python, and Looker Studio.
```

Do not initialize the remote repository with another README because this project already contains one.

In the VS Code terminal:

```powershell
git init
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/saas-growth-retention-analytics.git
```

Create staged commits rather than uploading everything as one commit:

```powershell
git add README.md START_HERE.md LICENSE .gitignore requirements.txt Makefile
git commit -m "chore: initialize repository and business case"

git add scripts data
git commit -m "feat: add reproducible synthetic SaaS data"

git add dbt/models/staging dbt/dbt_project.yml dbt/profiles.example.yml
git commit -m "feat: add dbt staging models and source tests"

git add dbt/models/intermediate
git commit -m "feat: model activation revenue retention and support"

git add dbt/models/marts
git commit -m "feat: add decision-ready marketing product and customer marts"

git add sql docs assets .github
git commit -m "analysis: quantify growth opportunity and publish executive case"

git push -u origin main
```

This history shows problem framing, data construction, modelling, analysis, and communication as separate work stages.

## 4. Create the BigQuery workspace

Use a Google Cloud project dedicated to this portfolio. Create a BigQuery dataset named `raw_saas` in the `US` location.

Authenticate locally:

```powershell
gcloud auth application-default login
```

Load the raw tables:

```powershell
python scripts/load_csv_to_bigquery.py --project YOUR_GCP_PROJECT --dataset raw_saas
```

Confirm that all seven tables appear under `raw_saas` and that the row counts are approximately:

| Table | Rows |
|---|---:|
| accounts | 12,000 |
| marketing_touches | 23,921 |
| product_events | 521,921 |
| subscriptions | 12,000 |
| invoices | 55,318 |
| support_tickets | 12,756 |
| campaign_spend | 273 |

## 5. Run the dbt project

Copy `dbt/profiles.example.yml` to your user dbt folder as `profiles.yml`, then replace `YOUR_GCP_PROJECT`.

In PowerShell:

```powershell
cd dbt
dbt debug
dbt build
```

The project creates three modelling layers:

### Staging

Standardizes source fields and types. This demonstrates clean warehouse interfaces rather than analyzing raw CSVs directly.

### Intermediate

Creates reusable account-level logic:

- `int_account_activation`
- `int_account_revenue`
- `int_account_retention`
- `int_account_support`

### Marts

Creates decision-ready tables:

- `fct_growth_funnel`
- `mart_channel_performance`
- `mart_activation_drivers`
- `mart_cohort_retention`
- `mart_customer_health`

After `dbt build`, capture one screenshot showing successful models and tests. Save it in `assets/` and add it to the README.

## 6. Validate the business logic

Open `sql/analysis/` and run the queries in numerical order.

### Query 1: Executive funnel

Use this to establish the size and conversion of the lifecycle:

- 12,000 signups
- 51.9% activation
- 46.8% trial-to-paid conversion
- 81.2% overall 90-day retention among paid accounts

### Query 2: Channel decision matrix

Use this to compare spend with downstream customer quality. The important synthetic findings are:

- Referral: 6.86x observed revenue-to-spend
- Organic Search: 6.85x
- Paid Search: 0.79x
- Paid Social: 0.40x

Do not conclude that attribution proves causality. State that these results identify where to investigate and experiment.

### Query 3: Activation and retention

The strongest finding is:

- Activated paid accounts: 86.4% 90-day retention
- Non-activated paid accounts: 65.2% 90-day retention

The 21.2-percentage-point difference is descriptive evidence that activation is a strong early indicator. It is not proof that forcing the actions will cause the entire retention difference.

### Query 4: Experiment population

This produces Paid Search and Paid Social trials that did not activate. It turns the analysis into an operational recommendation rather than ending with a chart.

## 7. Build the Looker Studio report

Create one report called:

```text
SaaS Growth Analytics — Acquisition to Retention
```

Connect Looker Studio to the BigQuery marts. Build four pages.

### Page 1: Executive Overview

The viewer should understand the decision in 30 seconds.

Include:

- Signups
- Activation rate
- Trial-to-paid rate
- 90-day retention
- Funnel from signup to retained account
- Revenue-to-spend by channel
- Three recommended actions

Write this takeaway at the top:

> Referral delivers the strongest customer economics, while Paid Social requires onboarding and targeting optimization. Growth planning should use retained CAC rather than signups or platform conversions alone.

### Page 2: Acquisition and Unit Economics

Include channel spend, paid accounts, CAC, retained CAC, realized revenue, revenue-to-spend, and 90-day retention.

The page must answer: **Where should the next marketing dollar be tested?**

### Page 3: Activation Funnel

Show completion of `created_project`, `invited_teammate`, and `connected_integration`, segmented by acquisition channel and company size.

The page must answer: **Which onboarding behaviour should Product influence?**

### Page 4: Retention and Customer Health

Show cohort retention, activated versus non-activated retention, health scores, and a prioritized intervention table.

The page must answer: **Which accounts need action now?**

Add a visible “Synthetic Data” label to every page.

## 8. Communicate the recommendation like a senior analyst

Use this structure in the README, dashboard, and interviews:

### Evidence

Activated paid accounts retained at 86.4%, versus 65.2% for non-activated paid accounts. Paid Social also produced the weakest observed revenue efficiency among the scaled paid channels.

### Interpretation

The company appears to have both an acquisition-quality problem and a time-to-value problem. Increasing trial volume without improving activation may create more low-retention customers.

### Recommendation

Launch a day-3 onboarding experiment for under-activated Paid Search and Paid Social trials. Make teammate invitation and integration connection explicit milestones. Do not reallocate material budget until incremental retained CAC is measured.

### Quantified planning scenario

A 10-percentage-point Paid Social activation improvement is associated with approximately 81 additional 90-day retained paid accounts and about $95,945 in annualized recurring revenue in the synthetic scenario.

### Limitation

The estimate applies observed differences as a scenario assumption. A randomized experiment is required to produce a causal estimate.

That final limitation is important. It demonstrates analytical judgment rather than overstating the result.

## 9. Finish the README

Replace these placeholders:

- `[Your Name]`
- `YOUR_LINKEDIN_URL`
- `YOUR_PORTFOLIO_URL`
- `YOUR_EMAIL`
- `YOUR_GCP_PROJECT`

Then add:

- A public Looker Studio link directly below the title
- Three real dashboard screenshots
- A successful dbt test screenshot
- One sentence explaining your personal role: “I designed the business case, generated the data, modelled the warehouse, conducted the analysis, and translated the findings into an experiment and budget recommendation.”

## 10. Publish and pin it

On your GitHub profile, pin this repository first. Use the repository topics:

```text
marketing-analytics
customer-analytics
product-analytics
saas
bigquery
dbt
sql
looker-studio
retention
customer-lifetime-value
```

When sharing it in an application, do not say “Here is my dashboard.” Say:

> I built an end-to-end SaaS growth case that connects acquisition spend to product activation, subscription revenue, and 90-day retention. The analysis ends with a testable onboarding recommendation and retained-CAC decision framework.
