"""Abstract base class for all data processors."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from pyspark.sql import DataFrame, SparkSession


@dataclass
class ProcessingConfig:
    """Common configuration shared by all processors."""

    source_path: str
    target_path: str
    source_format: str = "delta"
    target_format: str = "delta"
    write_mode: str = "overwrite"
    options: dict[str, Any] = field(default_factory=dict)


class BaseProcessor(ABC):
    """Abstract processor – subclasses implement :meth:`transform`."""

    def __init__(self, spark: SparkSession, config: ProcessingConfig) -> None:
        self.spark = spark
        self.config = config

    def read(self) -> DataFrame:
        """Read data from the source layer (Bronze or Silver)."""
        return (
            self.spark.read.format(self.config.source_format)
            .options(**self.config.options)
            .load(self.config.source_path)
        )

    @abstractmethod
    def transform(self, df: DataFrame) -> DataFrame:
        """Apply business logic transformations to the DataFrame."""

    def write(self, df: DataFrame) -> None:
        """Persist the transformed DataFrame to the target layer."""
        (
            df.write.format(self.config.target_format)
            .mode(self.config.write_mode)
            .options(**self.config.options)
            .save(self.config.target_path)
        )

    def process(self) -> None:
        """Orchestrate a full read → transform → write cycle."""
        raw_df = self.read()
        transformed_df = self.transform(raw_df)
        self.write(transformed_df)
