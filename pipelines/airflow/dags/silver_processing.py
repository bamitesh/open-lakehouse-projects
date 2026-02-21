"""Airflow DAG – Bronze → Silver processing pipeline."""

from __future__ import annotations

from datetime import datetime, timedelta

from airflow.decorators import dag, task


@dag(
    dag_id="silver_processing",
    description="Cleanse and standardise Bronze data into the Silver layer.",
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args={
        "owner": "lakehouse",
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
    },
    tags=["silver", "processing"],
)
def silver_processing_dag():
    @task()
    def run_silver_processor(source: str = "data/bronze", target: str = "data/silver") -> str:
        """Invoke the SilverProcessor Spark job."""
        return target

    @task()
    def run_dbt_silver_models(processed_path: str) -> bool:
        """Trigger dbt to materialise Silver models."""
        return True

    processed = run_silver_processor()
    run_dbt_silver_models(processed)


silver_processing_dag()
