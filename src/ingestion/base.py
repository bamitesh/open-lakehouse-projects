"""Abstract base class for all ingestion sources."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from pyspark.sql import DataFrame, SparkSession


@dataclass
class IngestionConfig:
    """Common configuration shared by all ingesters."""

    source_name: str
    target_path: str
    target_format: str = "delta"
    write_mode: str = "append"
    options: dict[str, Any] = field(default_factory=dict)


class BaseIngester(ABC):
    """Abstract ingester – all concrete ingesters must implement :meth:`ingest`."""

    def __init__(self, spark: SparkSession, config: IngestionConfig) -> None:
        self.spark = spark
        self.config = config

    @abstractmethod
    def read(self) -> DataFrame:
        """Read raw data from the source and return a Spark DataFrame."""

    def write(self, df: DataFrame) -> None:
        """Write a DataFrame to the Bronze layer in Delta format."""
        (
            df.write.format(self.config.target_format)
            .mode(self.config.write_mode)
            .options(**self.config.options)
            .save(self.config.target_path)
        )

    def ingest(self) -> None:
        """Orchestrate a full read → write cycle."""
        df = self.read()
        self.write(df)
