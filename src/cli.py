"""Typer-based CLI entry-point for the Open Lakehouse."""

import typer

app = typer.Typer(
    name="lakehouse",
    help="Open Lakehouse CLI – run ingestion, processing, and quality checks.",
)


@app.command()
def ingest(
    source: str = typer.Argument(..., help="Source path or connection string"),
    target: str = typer.Argument(..., help="Target Bronze layer path"),
    fmt: str = typer.Option("csv", "--format", "-f", help="Source file format"),
) -> None:
    """Ingest data from SOURCE into the Bronze layer at TARGET."""
    typer.echo(f"Ingesting '{source}' → '{target}' (format={fmt})")


@app.command()
def process(
    layer: str = typer.Argument(..., help="Target layer: silver | gold"),
    source: str = typer.Argument(..., help="Source layer path"),
    target: str = typer.Argument(..., help="Target layer path"),
) -> None:
    """Run a processing job to promote data to LAYER."""
    typer.echo(f"Processing '{source}' → '{target}' (layer={layer})")


if __name__ == "__main__":
    app()
