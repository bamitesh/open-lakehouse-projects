"""Shared pytest fixtures."""

import pytest


@pytest.fixture(scope="session")
def spark():
    """Provide a local SparkSession for unit tests."""
    from pyspark.sql import SparkSession

    session = (
        SparkSession.builder.master("local[1]")
        .appName("lakehouse-tests")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.default.parallelism", "1")
        .getOrCreate()
    )
    session.sparkContext.setLogLevel("WARN")
    yield session
    session.stop()
