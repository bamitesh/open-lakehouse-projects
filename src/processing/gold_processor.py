"""Gold-layer processor – aggregate Silver data into business-ready datasets."""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from .base import BaseProcessor


class GoldProcessor(BaseProcessor):
    """Apply business aggregations and enrichments to a Silver DataFrame.

    Override :meth:`transform` in a subclass to add domain-specific logic.
    """

    def transform(self, df: DataFrame) -> DataFrame:
        # Default pass-through; override in domain-specific subclasses.
        return df.withColumn("_gold_processed_at", F.current_timestamp())
