from typing import List

from github import Auth, Github

from src.clients.code_trackers.base import ICodeTracker
from src.shared.dtos import CommitData, PullRequestData


class GitHubClient(ICodeTracker):
    def __init__(self, access_token: str, repo_name: str) -> None:
        """Initialize the GitHub client.

        Args:
            access_token (str): The access token to authenticate with GitHub.
            repo_name (str): The name of the repository.
        """
        self.auth = Auth.Token(access_token)
        self.github = Github(auth=self.auth)
        self.repo_name = repo_name

    def get_pull_request(self, pr_id: int) -> PullRequestData:
        """Get pull request information.

        Args:
            pr_id (int): The ID of the pull request.

        Returns:
            PullRequestData: The pull request information.
        """
        repo = self.github.get_repo(self.repo_name)
        pr = repo.get_pull(pr_id)
        return PullRequestData(
            number=pr.number,
            title=pr.title,
            branch_name=pr.head.ref,
            state=pr.state,
            url=pr.html_url,
            repo_name=self.repo_name,
        )

    def get_pull_commits(self, pr_id: int) -> List[CommitData]:
        """Fetch commits for a PR.

        Args:
            pr_id (int): The ID of the pull request.

        Returns:
            List[CommitData]: List of commits in the pull request.
        """
        repo = self.github.get_repo(self.repo_name)
        pr = repo.get_pull(pr_id)
        commits = []
        for c in pr.get_commits():
            commits.append(
                CommitData(
                    hash=c.sha,
                    message=c.commit.message,
                    author=c.commit.author.name if c.commit.author else "unknown",
                    date=(
                        c.commit.author.date.isoformat()
                        if c.commit.author
                        else "unknown"
                    ),
                )
            )
        return commits

    def get_branch_commits(self, branch_name: str) -> List[CommitData]:
        """Get commits for a branch.

        Args:
            branch_name (str): The name of the branch.

        Returns:
            List[CommitData]: List of commits in the branch.
        """
        repo = self.github.get_repo(self.repo_name)
        commits = []
        for c in repo.get_commits(sha=branch_name):
            commits.append(
                CommitData(
                    hash=c.sha,
                    message=c.commit.message,
                    author=c.commit.author.name if c.commit.author else "unknown",
                    date=(
                        c.commit.author.date.isoformat()
                        if c.commit.author
                        else "unknown"
                    ),
                )
            )
        return commits

    def get_commit(self, commit_hash: str) -> CommitData:
        """Get a specific commit.

        Args:
            commit_hash (str): The hash of the commit.

        Returns:
            CommitData: The commit data.
        """
        repo = self.github.get_repo(self.repo_name)
        c = repo.get_commit(commit_hash)
        return CommitData(
            hash=c.sha,
            message=c.commit.message,
            author=c.commit.author.name if c.commit.author else "unknown",
            date=(c.commit.author.date.isoformat() if c.commit.author else "unknown"),
        )
