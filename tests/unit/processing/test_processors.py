"""Unit tests for SilverProcessor and GoldProcessor."""

import pytest
from pyspark.sql import SparkSession, Row

from src.processing.silver_processor import SilverProcessor
from src.processing.gold_processor import GoldProcessor
from src.processing.base import ProcessingConfig


class TestSilverProcessor:
    def test_transform_deduplicates(self, spark: SparkSession):
        df = spark.createDataFrame(
            [Row(id=1, val="a"), Row(id=1, val="a"), Row(id=2, val="b")]
        )
        config = ProcessingConfig(source_path="/tmp/s", target_path="/tmp/t")
        processor = SilverProcessor(spark, config)
        result = processor.transform(df)
        assert result.count() == 2

    def test_transform_adds_audit_columns(self, spark: SparkSession):
        df = spark.createDataFrame([Row(id=1)])
        config = ProcessingConfig(source_path="/tmp/s", target_path="/tmp/t")
        processor = SilverProcessor(spark, config)
        result = processor.transform(df)
        assert "_ingested_at" in result.columns


class TestGoldProcessor:
    def test_transform_adds_processed_column(self, spark: SparkSession):
        df = spark.createDataFrame([Row(id=1)])
        config = ProcessingConfig(source_path="/tmp/s", target_path="/tmp/t")
        processor = GoldProcessor(spark, config)
        result = processor.transform(df)
        assert "_gold_processed_at" in result.columns
