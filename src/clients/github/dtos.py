from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CommitData:
    hash: str
    message: str
    author: str
    date: str


@dataclass
class PullRequestData:
    number: int
    title: str
    branch_name: str
    state: str
    url: str
    commits: List[CommitData] = field(default_factory=list)
    summary: Optional[str] = None
    repo_name: Optional[str] = None
