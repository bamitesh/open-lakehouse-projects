"""Silver-layer processor – cleanse and standardise raw Bronze data."""

import pyspark.sql.functions as F
from pyspark.sql import DataFrame

from .base import BaseProcessor


class SilverProcessor(BaseProcessor):
    """Deduplicate, cast types, and add audit columns to a Bronze DataFrame."""

    def transform(self, df: DataFrame) -> DataFrame:
        return (
            df.dropDuplicates()
            .withColumn("_ingested_at", F.current_timestamp())
            .withColumn("_source_file", F.input_file_name())
        )
