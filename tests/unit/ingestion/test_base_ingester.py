"""Unit tests for ingestion base classes."""

import pytest
from pyspark.sql import SparkSession

from src.ingestion.base import BaseIngester, IngestionConfig


class _ConcreteIngester(BaseIngester):
    """Minimal concrete implementation for testing."""

    def read(self):
        return self.spark.createDataFrame(
            [{"id": 1, "value": "a"}, {"id": 2, "value": "b"}]
        )


class TestIngestionConfig:
    def test_defaults(self):
        config = IngestionConfig(source_name="s3://bucket/raw", target_path="s3://bucket/bronze")
        assert config.target_format == "delta"
        assert config.write_mode == "append"
        assert config.options == {}

    def test_custom_options(self):
        config = IngestionConfig(
            source_name="s3://bucket/raw",
            target_path="s3://bucket/bronze",
            options={"header": "true"},
        )
        assert config.options["header"] == "true"


class TestBaseIngester:
    def test_read_returns_dataframe(self, spark: SparkSession):
        config = IngestionConfig(source_name="/tmp/src", target_path="/tmp/bronze")
        ingester = _ConcreteIngester(spark, config)
        df = ingester.read()
        assert df.count() == 2

    def test_ingest_calls_read_and_write(self, spark: SparkSession, tmp_path):
        config = IngestionConfig(
            source_name="/tmp/src",
            target_path=str(tmp_path / "bronze"),
            target_format="parquet",
        )
        ingester = _ConcreteIngester(spark, config)
        ingester.ingest()
        result = spark.read.parquet(str(tmp_path / "bronze"))
        assert result.count() == 2
