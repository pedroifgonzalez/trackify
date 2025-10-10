from typing import Any, Dict, List, Protocol


class TrackerClient(Protocol):
    """Interface for repository-based trackers like GitHub."""

    def get_pull_request(self, pr_id: int) -> Dict[str, Any]: ...

    def get_pull_commits(self, pr_id: int) -> List[Dict[str, Any]]: ...

    def get_branch_commits(self, branch_name: str) -> List[Dict[str, Any]]: ...

    def get_commit(self, commit_hash: str) -> Dict[str, Any]: ...


class TimeTracker(Protocol):
    """Interface for time-tracking systems like WakaTime."""

    def get_total_time(self, entity_type: str, entity_id: str | int) -> float: ...


class LoggerClient(Protocol):
    """Interface for logging or recording time entries."""

    def create_time_entry(self, description: str, hours: float) -> None: ...


class ReportGeneratorClient(Protocol):
    """Interface for logging or recording time entries."""

    def add_commits(self, commits: List[Any]) -> None: ...

    def add_summary(self) -> None: ...

    def export_markdown(self) -> str: ...
