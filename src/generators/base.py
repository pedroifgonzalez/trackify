from typing import Callable


class FluentBase:
    """Base class to support fluent chaining."""

    def pipe(self, func: Callable[["FluentBase"], None]) -> "FluentBase":
        """Allows external functions to enrich the object."""
        func(self)
        return self

    def __repr__(self) -> str:
        cls = self.__class__.__name__
        return f"<{cls} {vars(self)}>"
