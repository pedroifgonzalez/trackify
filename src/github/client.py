from dataclasses import dataclass
from typing import Dict, Any, Optional, List, Tuple
import subprocess
import sys
import json
import os
from github import Github
from github import Auth


@dataclass
class PullRequestInfo:
    title: str
    branch_name: str
    state: str


class GitHubClient:
    def __init__(self, access_token, repo_name):
        self.auth = Auth.Token(access_token)
        self.github = Github(auth=self.auth)
        self.repo_name = repo_name

    def get_pull_request(self, pr_id: int) -> Optional[PullRequestInfo]:
        """Get pull request information

        Args:
            pr_id (str): The ID of the pull request.

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
