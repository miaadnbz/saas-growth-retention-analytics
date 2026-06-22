# GitHub Publishing Checklist

## Before publishing

- Replace `[Your Name]`, LinkedIn, portfolio, and email placeholders.
- Create the public Looker Studio report and add its URL near the top of the README.
- Replace the wireframe with three real dashboard screenshots.
- Run `python scripts/generate_synthetic_data.py` and confirm row counts.
- Run `dbt build` and add a screenshot of the successful test run.
- Replace `YOUR_GCP_PROJECT` in example SQL only after confirming no credentials are present.
- Never commit `profiles.yml`, service-account JSON, `.env`, or tokens.

## Suggested commit history

1. `chore: initialize repository and business case`
2. `feat: add reproducible synthetic SaaS source data`
3. `feat: add dbt staging models and source tests`
4. `feat: model activation revenue and retention`
5. `feat: add marketing product and customer marts`
6. `analysis: quantify channel economics and activation opportunity`
7. `docs: add executive brief measurement plan and dashboard guide`
8. `docs: publish Looker Studio dashboard and final screenshots`

A staged history shows how you work. Do not upload the complete project as one unexplained commit.
