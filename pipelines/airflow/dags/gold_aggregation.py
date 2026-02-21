"""Airflow DAG – Silver → Gold aggregation pipeline."""

from __future__ import annotations

from datetime import datetime, timedelta

from airflow.decorators import dag, task


@dag(
    dag_id="gold_aggregation",
    description="Aggregate Silver data into business-ready Gold datasets.",
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args={
        "owner": "lakehouse",
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
    },
    tags=["gold", "aggregation"],
)
def gold_aggregation_dag():
    @task()
    def run_gold_processor(source: str = "data/silver", target: str = "data/gold") -> str:
        """Invoke the GoldProcessor Spark job."""
        return target

    @task()
    def run_dbt_gold_models(processed_path: str) -> bool:
        """Trigger dbt to materialise Gold models."""
        return True

    @task()
    def notify_downstream(success: bool) -> None:
        """Notify downstream consumers that Gold data is ready."""

    processed = run_gold_processor()
    success = run_dbt_gold_models(processed)
    notify_downstream(success)


gold_aggregation_dag()
