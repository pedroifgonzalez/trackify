from datetime import datetime
from typing import Any, Dict, Optional

from src.clients.activity_trackers.base import IActivityTracker
from src.clients.code_trackers.base import ICodeTracker
from src.clients.time_managers.base import ITimeManager
from src.core.base import FluentBase
from src.generators.summaries.pullrequest import PullRequestReport


class Orchestrator(FluentBase):
    """A fluent, dependency-agnostic orchestrator to coordinate tracking flows."""

    def __init__(self) -> None:
        """Initialize the orchestrator."""
        self.dependencies: Dict[str, Any] = {}
        self.context: Dict[str, Any] = {}

    def with_code_tracker(self, code_tracker: ICodeTracker) -> "Orchestrator":
        """Add a code tracker.

        Args:
            code_tracker (ICodeTracker): The code tracker to add.

        Returns:
            Orchestrator: The orchestrator instance.
        """
        self.dependencies["code_tracker"] = code_tracker
        return self

    def with_time_manager(self, time_manager: ITimeManager) -> "Orchestrator":
        """Add a time manager.

        Args:
            time_manager (ITimeManager): The time manager to add.

        Returns:
            Orchestrator: The orchestrator instance.
        """
        self.dependencies["time_manager"] = time_manager
        return self

    def with_activity_tracker(
        self, activity_tracker: IActivityTracker
    ) -> "Orchestrator":
        """Add an activity tracker.

        Args:
            activity_tracker (IActivityTracker): The activity tracker to add.

        Returns:
            Orchestrator: The orchestrator instance.
        """
        self.dependencies["activity_tracker"] = activity_tracker
        return self

    def with_report_generator(
        self, report_generator: PullRequestReport
    ) -> "Orchestrator":
        """Add a report generator.

        Args:
            report_generator (PullRequestReport): The report generator to add.

        Returns:
            Orchestrator: The orchestrator instance.
        """
        self.dependencies["report_generator"] = report_generator
        return self

    def get_pull(self, pr_id: int) -> "Orchestrator":
        """Get pull request and commits.

        Args:
            pr_id (int): The ID of the pull request.

        Returns:
            Orchestrator: The orchestrator instance.
        """
        code_tracker = self._require("code_tracker")
        pr = code_tracker.get_pull_request(pr_id)
        commits = code_tracker.get_pull_commits(pr_id)
        self.context.update(
            {
                "pr": pr,
                "commits": commits,
                "branch_name": pr.branch_name,
                "repo_name": pr.repo_name,
            }
        )
        return self

    def get_branch(self, branch_name: str) -> "Orchestrator":
        """Get branch commits.

        Args:
            branch_name (str): The name of the branch.

        Returns:
            Orchestrator: The orchestrator instance.
        """
        code_tracker = self._require("code_tracker")
        commits = code_tracker.get_branch_commits(branch_name)
        self.context.update(
            {
                "commits": commits,
                "branch_name": branch_name,
                "repo_name": branch_name,
            }
        )
        return self

    def get_commit(self, commit_hash: str) -> "Orchestrator":
        """Get commit.

        Args:
            commit_hash (str): The hash of the commit.

        Returns:
            Orchestrator: The orchestrator instance.
        """
        code_tracker = self._require("code_tracker")
        commit = code_tracker.get_commit(commit_hash)
        self.context.update(
            {
                "commit": commit,
                "branch_name": commit.branch_name,
                "repo_name": commit.repo_name,
            }
        )
        return self

    def compute_time(self, search_date: Optional[datetime] = None) -> "Orchestrator":
        """Compute total time for the specified branch and project.

        Args:
            search_date (Optional[datetime], optional): The date to search for time data. Defaults to None.

        Raises:
            ValueError: If branch name or repo name are missing from context.
            ValueError: If no time data is found for the specified branch and project.

        Returns:
            Orchestrator: The orchestrator instance.
        """
        activity_tracker = self._require("activity_tracker")
        if not self.context.get("branch_name") or not self.context.get("repo_name"):
            raise ValueError("Branch name or repo name missing from context.")
        branch_name = self.context["branch_name"]
        project_name = self.context["repo_name"].split("/")[-1]
        total_time = activity_tracker.get_total_time(
            branch_name=branch_name,
            project_name=project_name,
            search_date=search_date,
        )
        if not total_time:
            raise ValueError("No time data found for the specified branch and project.")
        self.context["start"] = total_time.start
        self.context["end"] = total_time.end
        self.context["duration"] = total_time.duration
        return self

    def add_summary(self) -> "Orchestrator":
        """Add summary to context.

        Raises:
            ValueError: If commits or PR are missing from context.

        Returns:
            Orchestrator: The orchestrator instance.
        """
        report_generator = self._require("report_generator")
        if not self.context.get("commits") or not self.context.get("pr"):
            raise ValueError("Commits or PR missing from context.")
        report_generator.add_pr(self.context["pr"])
        report_generator.add_commits(self.context["commits"])
        report_generator.add_summary()
        self.context["summary"] = report_generator.export_markdown()
        return self

    def log_time(self) -> "Orchestrator":
        """Log time entry.

        Raises:
            ValueError: If summary or hours are missing from context.

        Returns:
            Orchestrator: The orchestrator instance.
        """
        time_manager = self._require("time_manager")
        summary = self.context.get("summary")
        start = self.context.get("start")
        end = self.context.get("end")
        if not any([summary, start, end]):
            raise ValueError("Summary or hours missing from context.")
        time_manager.create_time_entry(description=summary, start=start, end=end)
        return self

    def _require(self, name: str) -> Any:
        """Get a dependency by name.

        Args:
            name (str): The name of the dependency.

        Raises:
            RuntimeError: If the dependency is not provided.

        Returns:
            Any: The dependency.
        """
        if name not in self.dependencies:
            raise RuntimeError(f"Dependency '{name}' is required but not provided.")
        return self.dependencies[name]
