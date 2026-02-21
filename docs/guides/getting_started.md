# Getting Started

## Prerequisites

- Python 3.11+
- Docker & Docker Compose
- (Optional) Terraform 1.7+

## Quick Start – Local Development

### 1. Clone the repository

```bash
git clone https://github.com/bamitesh/open-lakehouse-projects.git
cd open-lakehouse-projects
```

### 2. Install Python dependencies

```bash
make install-dev
```

### 3. Start the local stack

```bash
make docker-up
```

This starts:
- **MinIO** at <http://localhost:9001> (credentials: `minioadmin` / `minioadmin`)
- **Spark** master at <http://localhost:4040>
- **Airflow** at <http://localhost:8080> (credentials: `admin` / `admin`)
- **Jupyter** at <http://localhost:8888>

### 4. Run the ingestion pipeline

```bash
lakehouse ingest path/to/source.csv data/bronze/source_a --format csv
```

### 5. Run tests

```bash
make test
```

## Project Layout

```
open-lakehouse-projects/
├── src/                  # Python source code
│   ├── ingestion/        # Bronze layer ingesters
│   ├── processing/       # Silver & Gold processors
│   ├── serving/          # Query helpers
│   ├── catalog/          # Catalog client
│   └── utils/            # Shared utilities
├── pipelines/
│   └── airflow/dags/     # Airflow DAG definitions
├── dbt/                  # dbt project (models, tests, macros)
├── data/                 # Local data directories (bronze/silver/gold)
├── infrastructure/
│   ├── docker/           # Docker Compose for local dev
│   └── terraform/        # IaC for cloud deployment
├── notebooks/            # Jupyter notebooks
├── tests/                # Pytest test suite
├── configs/              # Environment configuration files
└── docs/                 # Project documentation
```
