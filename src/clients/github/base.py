from abc import ABC, abstractmethod
from typing import Callable, List

from src.clients.github.dtos import CommitData, PullRequestData


class IGitClient(ABC):
    @abstractmethod
    def get_pull_request(self, pr_id: int) -> PullRequestData: ...
    @abstractmethod
    def get_pull_commits(self, pr_id: int) -> List[CommitData]: ...


class FluentBase:
    """Base class to support fluent chaining."""

    def pipe(self, func: Callable[["FluentBase"], None]) -> "FluentBase":
        """Allows external functions to enrich the object."""
        func(self)
        return self

    def __repr__(self) -> str:
        cls = self.__class__.__name__
        return f"<{cls} {vars(self)}>"
