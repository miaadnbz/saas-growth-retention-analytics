"""Load generated CSV source tables into BigQuery.

Usage:
    python scripts/load_csv_to_bigquery.py --project my-project --dataset raw_saas

Authentication:
    gcloud auth application-default login
"""
from __future__ import annotations
import argparse
from pathlib import Path
from google.cloud import bigquery


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', required=True)
    parser.add_argument('--dataset', default='raw_saas')
    parser.add_argument('--location', default='US')
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    data_dir = root / 'data' / 'raw'
    client = bigquery.Client(project=args.project)
    dataset_ref = bigquery.Dataset(f'{args.project}.{args.dataset}')
    dataset_ref.location = args.location
    client.create_dataset(dataset_ref, exists_ok=True)

    for csv_path in sorted(data_dir.glob('*.csv')):
        table_id = f'{args.project}.{args.dataset}.{csv_path.stem}'
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=True,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        )
        with csv_path.open('rb') as source_file:
            job = client.load_table_from_file(source_file, table_id, job_config=job_config)
        job.result()
        table = client.get_table(table_id)
        print(f'Loaded {table_id}: {table.num_rows:,} rows')


if __name__ == '__main__':
    main()
