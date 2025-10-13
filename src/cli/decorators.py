"""CLI decorators for error handling and common functionality."""

import logging
from functools import wraps
from typing import Any, Callable

import typer
from rich.console import Console

from src.core.exceptions import TrackifyError

console = Console()
logger = logging.getLogger("trackify")


def handle_errors(func: Callable) -> Any:
    """Decorator to handle errors in CLI commands.

    Catches TrackifyError and generic exceptions, logs them,
    displays user-friendly messages, and exits with code 1.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except TrackifyError as e:
            logger.error(f"Trackify error: {e}")
            console.print(f"[bold red]Error:[/bold red] {e}")
            raise typer.Exit(code=1)
        except Exception as e:
            logger.exception("Unexpected error occurred.")
            console.print(
                "[bold red]Unexpected error:[/bold red] Something went wrong. "
                "Use --debug for more info."
            )
            raise typer.Exit(code=1)

    return wrapper
