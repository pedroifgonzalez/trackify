import json
import os
import subprocess
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from github import Auth, Github


@dataclass
class PullRequestInfo:
    title: str
    branch_name: str
    state: str


class GitHubClient:
    def __init__(self, access_token: str, repo_name: str) -> None:
        """Initialize the GitHub client.

        Args:
            access_token (str): The access token to authenticate with GitHub.
            repo_name (str): The name of the repository.
        """
        self.auth = Auth.Token(access_token)
        self.github = Github(auth=self.auth)
        self.repo_name = repo_name

    def get_pull_request(self, pr_id: int) -> Optional[PullRequestInfo]:
        """Get pull request information.

        Args:
            pr_id (int): The ID of the pull request.

        Returns:
            Optional[PullRequestInfo]: The pull request information.
        """
        repo = self.github.get_repo(self.repo_name)
        pr = repo.get_pull(pr_id)
        return PullRequestInfo(
            title=pr.title,
            branch_name=pr.head.ref,
            state=pr.state,
        )
