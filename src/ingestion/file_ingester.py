"""File-based ingester – reads CSV / JSON / Parquet files into the Bronze layer."""

from pyspark.sql import DataFrame

from .base import BaseIngester, IngestionConfig


class FileIngester(BaseIngester):
    """Ingest structured files from a local or object-store path."""

    def __init__(self, spark, config: IngestionConfig, file_format: str = "csv") -> None:
        super().__init__(spark, config)
        self.file_format = file_format

    def read(self) -> DataFrame:
        return (
            self.spark.read.format(self.file_format)
            .options(**self.config.options)
            .load(self.config.source_name)
        )
