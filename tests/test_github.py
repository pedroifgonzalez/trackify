import os

import pytest

from src.clients.code_trackers.github.client import GitHubClient
from src.generators.summaries.pullrequest import PullRequestReport

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
REPO_NAME = os.getenv("REPO_NAME")


@pytest.mark.vcr
def test_get_pull_request():
    gh_client = GitHubClient(access_token=ACCESS_TOKEN, repo_name=REPO_NAME)
    pr = gh_client.get_pull_request(584)
    assert pr
    assert pr.title
    assert pr.branch_name
    assert pr.state


@pytest.mark.vcr
def test_get_pull_commits():
    gh_client = GitHubClient(access_token=ACCESS_TOKEN, repo_name=REPO_NAME)
    commits = gh_client.get_pull_commits(584)
    assert commits
    assert len(commits) > 0


@pytest.mark.vcr
def test_pull_request_report():
    gh_client = GitHubClient(access_token=ACCESS_TOKEN, repo_name=REPO_NAME)
    pr = gh_client.get_pull_request(584)
    commits = gh_client.get_pull_commits(584)
    report = (
        PullRequestReport(data=pr).add_commits(commits).add_summary().export_markdown()
    )
    assert report


@pytest.mark.vcr
def test_get_branch_commits():
    gh_client = GitHubClient(
        access_token=ACCESS_TOKEN, repo_name="pedroifgonzalez/trackify"
    )
    commits = gh_client.get_branch_commits("develop")
    assert commits
    assert len(commits) > 0


@pytest.mark.vcr
def test_get_commit():
    gh_client = GitHubClient(
        access_token=ACCESS_TOKEN, repo_name="pedroifgonzalez/trackify"
    )
    commit = gh_client.get_commit("6cd8df2129a48b57803bbae4e7d206d31f7ae71b")
    assert commit
