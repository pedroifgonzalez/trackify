from contextlib import contextmanager
from typing import Any, Callable, ContextManager, TypeVar

from rich.console import Console

T = TypeVar("T", bound="FluentBase")
console = Console()


class FluentBase:
    """Base class to support fluent chaining."""

    def stage(
        self: T, message: str, func: Callable[[T], Any] | str, *args: Any, **kwargs: Any
    ) -> T:
        """Execute an operation with a console status spinner.

        Wrapper around with_context with console.status for better readability.

        Args:
            message: Status message to display (without trailing "...")
            func: Either a callable that takes self, or a string method name to call
            *args: Positional arguments to pass if func is a string method name
            **kwargs: Keyword arguments. 'spinner' can be specified (default: "dots")

        Returns:
            T: The instance for method chaining

        Example:
            # Using a lambda
            orchestrator.stage("Initializing", lambda o: o.with_code_tracker(client))

            # Using a method name
            orchestrator.stage("Fetching PR", "get_pull", pr_id)

            # With custom spinner
            orchestrator.stage("Processing", "compute_time", spinner="point")
        """
        spinner = kwargs.pop("spinner", "dots")
        with console.status(f"[bold blue]{message}...", spinner=spinner):
            if isinstance(func, str):
                getattr(self, func)(*args, **kwargs)
            else:
                func(self)
        return self
