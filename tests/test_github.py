import pytest
from src.github.client import GitHubClient
import os
from conftest import trackify_vcr

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
REPO_NAME = os.getenv("REPO_NAME")


@trackify_vcr.use_cassette
def test_get_pull_request():
    gh_client = GitHubClient(access_token=ACCESS_TOKEN, repo_name=REPO_NAME)
    pr = gh_client.get_pull_request(584)
    assert pr
    assert pr.title
    assert pr.branch_name
    assert pr.state
