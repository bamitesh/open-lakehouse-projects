"""Schema registry – centralised column definitions shared across layers."""

from pyspark.sql.types import (
    StringType,
    StructField,
    StructType,
    TimestampType,
)

# Audit columns appended to every table in the lakehouse
AUDIT_SCHEMA = StructType(
    [
        StructField("_ingested_at", TimestampType(), nullable=False),
        StructField("_source_file", StringType(), nullable=True),
        StructField("_processed_at", TimestampType(), nullable=True),
    ]
)
