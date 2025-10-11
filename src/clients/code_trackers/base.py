from abc import ABC, abstractmethod
from typing import List

from src.shared.dtos import CommitData, PullRequestData


class ICodeTracker(ABC):
    """Interface for repository-based trackers like GitHub."""

    @abstractmethod
    def get_pull_request(self, pr_id: int) -> PullRequestData: ...

    @abstractmethod
    def get_pull_commits(self, pr_id: int) -> List[CommitData]: ...

    @abstractmethod
    def get_branch_commits(self, branch_name: str) -> List[CommitData]: ...

    @abstractmethod
    def get_commit(self, commit_hash: str) -> CommitData: ...
