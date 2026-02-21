# Open Lakehouse Projects

A **production-ready, opinionated project structure** for building a modern open data lakehouse.  
Designed to be used as a starting point for new projects and as a **cookiecutter template** in the future.

---

## ✨ Features

- **Medallion Architecture** – Bronze → Silver → Gold data layers
- **Apache Spark + Delta Lake** – scalable, ACID-compliant storage
- **dbt** – SQL-based transformations with built-in testing and documentation
- **Apache Airflow** – DAG-based orchestration for all pipelines
- **Great Expectations** – automated data quality validation
- **Terraform** – infrastructure-as-code for cloud deployment (AWS)
- **Docker Compose** – local development stack (Spark, Airflow, MinIO, Jupyter)
- **Typer CLI** – command-line interface for running pipelines

---

## 🏗 Project Structure

```
open-lakehouse-projects/
│
├── src/                        # Python source code
│   ├── ingestion/              # Bronze layer ingesters (file, API, streaming)
│   │   ├── base.py             # Abstract BaseIngester
│   │   └── file_ingester.py    # File-based ingester (CSV/JSON/Parquet)
│   ├── processing/             # Silver & Gold processors
│   │   ├── base.py             # Abstract BaseProcessor
│   │   ├── silver_processor.py # Cleanse & deduplicate (Silver)
│   │   └── gold_processor.py   # Aggregate & enrich (Gold)
│   ├── serving/                # Query helpers for downstream consumers
│   ├── catalog/                # Data catalog client (Hive / Unity)
│   │   └── client.py
│   ├── utils/                  # Shared utilities
│   │   ├── spark.py            # SparkSession factory
│   │   ├── logging.py          # Structured logging (loguru)
│   │   └── schema.py           # Shared schema / audit columns
│   └── cli.py                  # Typer-based CLI entry-point
│
├── pipelines/
│   └── airflow/
│       ├── dags/               # Airflow DAG definitions
│       │   ├── bronze_ingestion.py
│       │   ├── silver_processing.py
│       │   └── gold_aggregation.py
│       └── plugins/            # Custom Airflow operators / sensors
│
├── dbt/                        # dbt project
│   ├── models/
│   │   ├── bronze/             # Raw source models
│   │   ├── silver/             # Cleansed / staged models
│   │   └── gold/               # Business-ready models
│   ├── tests/                  # Custom dbt tests
│   ├── macros/                 # Reusable SQL macros
│   ├── seeds/                  # Static reference data
│   ├── dbt_project.yml
│   └── profiles.yml
│
├── data/                       # Local data directories (git-ignored contents)
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   └── sample/                 # Small sample datasets for local development
│
├── infrastructure/
│   ├── docker/
│   │   └── docker-compose.yml  # Local dev stack (Spark, Airflow, MinIO, Jupyter)
│   └── terraform/              # IaC for cloud deployment
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       ├── modules/
│       │   ├── storage/        # S3 buckets per layer
│       │   └── compute/        # EMR / Spark cluster
│       └── environments/
│           ├── dev/
│           └── prod/
│
├── notebooks/
│   ├── exploratory/            # EDA notebooks
│   └── data_quality/           # Data quality investigation notebooks
│
├── tests/
│   ├── conftest.py             # Shared fixtures (SparkSession)
│   ├── unit/
│   │   ├── ingestion/          # Unit tests for ingesters
│   │   └── processing/         # Unit tests for processors
│   ├── integration/            # Integration tests
│   └── e2e/                    # End-to-end pipeline tests
│
├── configs/
│   ├── default.yml             # Default configuration
│   ├── dev.yml                 # Development overrides
│   └── prod.yml                # Production overrides
│
├── docs/
│   ├── architecture/
│   │   └── overview.md         # Medallion architecture diagram
│   └── guides/
│       └── getting_started.md  # Quick-start guide
│
├── Makefile                    # Common developer commands
├── pyproject.toml              # Project metadata & dependencies
└── .gitignore
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose

### 1. Install dependencies

```bash
make install-dev
```

### 2. Start the local stack

```bash
make docker-up
```

| Service | URL | Credentials |
|---------|-----|-------------|
| Airflow | <http://localhost:8080> | admin / admin |
| Jupyter | <http://localhost:8888> | – |
| MinIO   | <http://localhost:9001> | minioadmin / minioadmin |
| Spark UI | <http://localhost:4040> | – |

### 3. Run the CLI

```bash
# Ingest a CSV file into the Bronze layer
lakehouse ingest path/to/data.csv data/bronze/my_table

# Promote Bronze → Silver
lakehouse process silver data/bronze/my_table data/silver/my_table
```

### 4. Run tests

```bash
make test          # all tests
make test-unit     # unit tests only
```

### 5. Run dbt

```bash
make dbt-run       # materialise all models
make dbt-test      # run dbt tests
make dbt-docs      # serve dbt documentation
```

---

## 🛠 Development

```bash
make lint        # ruff lint
make format      # ruff format
make typecheck   # mypy
```

---

## 📖 Documentation

- [Architecture Overview](docs/architecture/overview.md)
- [Getting Started Guide](docs/guides/getting_started.md)

---

## 📄 License

[MIT](LICENSE)