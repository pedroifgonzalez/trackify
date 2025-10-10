from datetime import datetime
from typing import Any, Dict, Optional

from src.base.interfaces import (
    LoggerClient,
    ReportGeneratorClient,
    TimeTracker,
    TrackerClient,
)


class Orchestrator:
    """A fluent, dependency-agnostic orchestrator to coordinate tracking flows."""

    def __init__(self) -> None:
        self.dependencies: Dict[str, Any] = {}
        self.context: Dict[str, Any] = {}

    # ----------------------------------------------------
    # Dependency Injection
    # ----------------------------------------------------
    def with_tracker(self, tracker: TrackerClient) -> "Orchestrator":
        self.dependencies["tracker"] = tracker
        return self

    def with_time_tracker(self, time_tracker: TimeTracker) -> "Orchestrator":
        self.dependencies["time_tracker"] = time_tracker
        return self

    def with_logger(self, logger: LoggerClient) -> "Orchestrator":
        self.dependencies["logger"] = logger
        return self

    def with_report_generator(
        self, report_generator: ReportGeneratorClient
    ) -> "Orchestrator":
        self.dependencies["report_generator"] = report_generator
        return self

    # ----------------------------------------------------
    # Core Fluent Operations
    # ----------------------------------------------------
    def get_pull(self, pr_id: int) -> "Orchestrator":
        tracker = self._require("tracker")
        pr = tracker.get_pull_request(pr_id)
        commits = tracker.get_pull_commits(pr_id)
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
        tracker = self._require("tracker")
        commits = tracker.get_branch_commits(branch_name)
        self.context.update(
            {
                "commits": commits,
                "branch_name": branch_name,
                "repo_name": branch_name,
            }
        )
        return self

    def get_commit(self, commit_hash: str) -> "Orchestrator":
        tracker = self._require("tracker")
        commit = tracker.get_commit(commit_hash)
        self.context.update(
            {
                "commit": commit,
                "branch_name": commit.branch_name,
                "repo_name": commit.repo_name,
            }
        )
        return self

    def compute_time(self, search_date: Optional[datetime] = None) -> "Orchestrator":
        time_tracker = self._require("time_tracker")
        if not self.context.get("branch_name") or not self.context.get("repo_name"):
            raise ValueError("Branch name or repo name missing from context.")
        branch_name = self.context["branch_name"]
        project = self.context["repo_name"].split("/")[-1]
        total_time = time_tracker.get_total_time(
            branch_name=branch_name,
            project=project,
            search_date=search_date,
        )
        if not total_time:
            raise ValueError("No time data found for the specified branch and project.")
        self.context["start"] = total_time.start
        self.context["end"] = total_time.end
        self.context["duration"] = total_time.duration
        return self

    def add_summary(self) -> "Orchestrator":
        report_generator = self._require("report_generator")
        if not self.context.get("commits") or not self.context.get("pr"):
            raise ValueError("Commits or PR missing from context.")
        report_generator.add_pr(self.context["pr"])
        report_generator.add_commits(self.context["commits"])
        report_generator.add_summary()
        self.context["summary"] = report_generator.export_markdown()
        return self

    def log_time(self) -> "Orchestrator":
        logger = self._require("logger")
        summary = self.context.get("summary")
        start = self.context.get("start")
        end = self.context.get("end")
        if not any([summary, start, end]):
            raise ValueError("Summary or hours missing from context.")
        logger.create_time_entry(description=summary, start=start, end=end)
        return self

    # ----------------------------------------------------
    # Internal Helper
    # ----------------------------------------------------
    def _require(self, name: str) -> Any:
        if name not in self.dependencies:
            raise RuntimeError(f"Dependency '{name}' is required but not provided.")
        return self.dependencies[name]
