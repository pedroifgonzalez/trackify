import os

import pytest

from src.cli.commands.config import config as cfg
from src.clients.activity_trackers.wakatime.client import WakaClient
from src.clients.code_trackers.github.client import GitHubClient
from src.clients.time_managers.clockify.client import ClockifyClient
from src.core.exceptions import OrchestratorError
from src.core.orchestrator import Orchestrator
from src.generators.summaries.pullrequest import PullRequestReport
from src.shared.dtos import PullRequestData


@pytest.mark.vcr
def test_get_branch():
    orchestrator = Orchestrator()
    (
        orchestrator.with_code_tracker(
            code_tracker=GitHubClient(
                access_token=cfg.GITHUB_ACCESS_TOKEN,
                repo_name="pedroifgonzalez/trackify",
            )
        ).get_branch("develop")
    )
    assert orchestrator.context.get("commits") is not None


@pytest.mark.vcr
def test_orchestrator_get_commit():
    orchestrator = Orchestrator()
    (
        orchestrator.with_code_tracker(
            code_tracker=GitHubClient(
                access_token=cfg.GITHUB_ACCESS_TOKEN,
                repo_name="pedroifgonzalez/trackify",
            )
        ).get_commit("17eb55f13de5130bd40bbee0146152845e415524")
    )
    assert orchestrator.context.get("commit") is not None


def test_compute_time_missing_dependency():
    orchestrator = Orchestrator()
    with pytest.raises(OrchestratorError):
        orchestrator.compute_time()


def test_compute_time_missing_branch_name():
    orchestrator = Orchestrator()
    orchestrator.with_activity_tracker(
        WakaClient(
            api_key=cfg.WAKATIME_API_KEY,
        )
    )
    with pytest.raises(OrchestratorError):
        orchestrator.compute_time()


def test_log_time_missing_summary_data():
    orchestrator = Orchestrator()
    orchestrator.with_time_manager(
        ClockifyClient(
            api_key=cfg.CLOCKIFY_API_KEY,
            project_id=cfg.CLOCKIFY_PROJECT_ID,
            workspace_id=cfg.CLOCKIFY_WORKSPACE_ID,
        )
    )
    with pytest.raises(OrchestratorError):
        orchestrator.log_time()


def test_add_summary_missing_pr():
    orchestrator = Orchestrator()
    orchestrator.with_report_generator(
        PullRequestReport(
            data=PullRequestData(
                commits=[],
                state="open",
                number=1,
                title="Test PR",
                branch_name="test-branch-name",
                url="test-url",
                repo_name="repo-name",
            )
        )
    )
    with pytest.raises(OrchestratorError):
        orchestrator.add_summary()
