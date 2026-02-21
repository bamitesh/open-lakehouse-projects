"""Data catalog client wrapper.

Provides a thin abstraction over a Hive / Unity / Iceberg catalog so
the rest of the codebase is not coupled to a specific implementation.
"""

import re
from dataclasses import dataclass
from pyspark.sql import SparkSession

# Only allow identifier characters to prevent SQL injection in catalog names.
_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_.]*$")


def _validate_identifier(value: str, field: str) -> str:
    """Raise ValueError if *value* is not a safe SQL identifier."""
    if not _IDENTIFIER_RE.match(value):
        raise ValueError(
            f"Invalid {field} '{value}': only letters, digits, underscores, and dots are allowed."
        )
    return value


@dataclass
class TableMetadata:
    """Lightweight representation of a catalog table entry."""

    catalog: str
    schema: str
    table: str
    location: str
    format: str = "delta"
    description: str = ""

    @property
    def full_name(self) -> str:
        return f"{self.catalog}.{self.schema}.{self.table}"


class CatalogClient:
    """Thin wrapper around SparkSession's catalog API."""

    def __init__(self, spark: SparkSession, catalog_name: str = "spark_catalog") -> None:
        self.spark = spark
        self.catalog_name = catalog_name

    def table_exists(self, schema: str, table: str) -> bool:
        return self.spark.catalog.tableExists(f"{schema}.{table}")

    def create_schema_if_not_exists(self, schema: str, location: str | None = None) -> None:
        _validate_identifier(schema, "schema")
        if location is not None:
            # location is an arbitrary path – embed via parameterised-style quoting
            escaped = location.replace("'", "\\'")
            self.spark.sql(f"CREATE SCHEMA IF NOT EXISTS {schema} LOCATION '{escaped}'")
        else:
            self.spark.sql(f"CREATE SCHEMA IF NOT EXISTS {schema}")

    def register_table(self, metadata: TableMetadata) -> None:
        _validate_identifier(metadata.catalog, "catalog")
        _validate_identifier(metadata.schema, "schema")
        _validate_identifier(metadata.table, "table")
        _validate_identifier(metadata.format, "format")
        escaped_desc = metadata.description.replace("'", "\\'")
        escaped_loc = metadata.location.replace("'", "\\'")
        self.spark.sql(
            f"""
            CREATE TABLE IF NOT EXISTS {metadata.full_name}
            USING {metadata.format}
            COMMENT '{escaped_desc}'
            LOCATION '{escaped_loc}'
            """
        )
