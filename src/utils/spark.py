"""Shared Spark session factory."""

from pyspark.sql import SparkSession


def get_spark_session(app_name: str = "OpenLakehouse", **kwargs) -> SparkSession:
    """Return a configured SparkSession.

    Extra keyword arguments are forwarded as Spark config entries.
    """
    builder = SparkSession.builder.appName(app_name)
    for key, value in kwargs.items():
        builder = builder.config(key, value)
    return builder.getOrCreate()
