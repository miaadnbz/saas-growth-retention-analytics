setup:
	python -m venv .venv
	.venv/bin/pip install -r requirements.txt

generate:
	.venv/bin/python scripts/generate_synthetic_data.py

dbt-build:
	cd dbt && dbt build

lint:
	sqlfluff lint dbt/models --dialect bigquery --templater dbt
