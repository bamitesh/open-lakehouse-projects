.PHONY: install install-dev lint format typecheck test test-unit test-integration clean docker-up docker-down

PYTHON := python3
PIP    := pip3

## ── Setup ─────────────────────────────────────────────────────────────────────
install:
	$(PIP) install -e .

install-dev:
	$(PIP) install -e ".[dev,dbt,airflow]"
	pre-commit install

## ── Quality ───────────────────────────────────────────────────────────────────
lint:
	ruff check src tests

format:
	ruff format src tests

typecheck:
	mypy src

## ── Tests ─────────────────────────────────────────────────────────────────────
test:
	pytest tests/ -v

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

## ── Docker ────────────────────────────────────────────────────────────────────
docker-up:
	docker compose -f infrastructure/docker/docker-compose.yml up -d

docker-down:
	docker compose -f infrastructure/docker/docker-compose.yml down

## ── dbt ───────────────────────────────────────────────────────────────────────
dbt-debug:
	cd dbt && dbt debug

dbt-run:
	cd dbt && dbt run

dbt-test:
	cd dbt && dbt test

dbt-docs:
	cd dbt && dbt docs generate && dbt docs serve

## ── Cleanup ───────────────────────────────────────────────────────────────────
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null; true
	find . -type f -name "*.pyc" -delete 2>/dev/null; true
	rm -rf .pytest_cache .mypy_cache .ruff_cache dist build *.egg-info
