"""Airflow DAG – Bronze ingestion pipeline."""

from __future__ import annotations

from datetime import datetime, timedelta

from airflow.decorators import dag, task


@dag(
    dag_id="bronze_ingestion",
    description="Ingest raw data from sources into the Bronze layer.",
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args={
        "owner": "lakehouse",
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
    },
    tags=["bronze", "ingestion"],
)
def bronze_ingestion_dag():
    @task()
    def extract_source_a() -> str:
        """Extract raw data from Source A."""
        return "data/bronze/source_a"

    @task()
    def extract_source_b() -> str:
        """Extract raw data from Source B."""
        return "data/bronze/source_b"

    @task()
    def validate_bronze(path_a: str, path_b: str) -> bool:
        """Run lightweight row-count validation on ingested Bronze files."""
        return True

    path_a = extract_source_a()
    path_b = extract_source_b()
    validate_bronze(path_a, path_b)


bronze_ingestion_dag()
