import typer
from rich.console import Console

from src.cli.commands.config import interactive_setup
from src.cli.commands.pr import pr_app

console = Console()
app = typer.Typer(help="Trackify CLI — Track coding work and context effortlessly.")

# Register command groups
app.add_typer(pr_app, name="pr")


@app.command()
def setup() -> None:
    """Interactive setup to configure Trackify with your API keys."""
    interactive_setup()


@app.callback()
def main() -> None:
    """Trackify — developer time and task orchestration tool."""
    console.print("[bold cyan]TRACKIFY[/bold cyan]", justify="center", style="bold")
    console.print("Your coding productivity companion.\n", justify="center")


if __name__ == "__main__":
    app()
