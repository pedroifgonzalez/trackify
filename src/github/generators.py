import re
from typing import Dict, List, Optional

from src.github.dtos import CommitData, PullRequestData

from .base import FluentBase


class PullRequestReport(FluentBase):
    """Enriched PullRequestDTO with summarization and analytics."""

    def __init__(
        self,
        data: Optional[PullRequestData] = None,
    ):
        self.context = {
            "commits": data.commits if data else [],
            "state": data.state if data else None,
            "number": data.number if data else None,
            "title": data.title if data else None,
            "branch_name": data.branch_name if data else None,
            "url": data.url if data else None,
        }

    def categorize_commit_message(self, message: str) -> str:
        """Categorize a commit message by prefix."""
        lower = message.lower()
        if lower.startswith("feat:"):
            return "✨ Feature"
        elif lower.startswith("fix:"):
            return "🐛 Fix"
        elif lower.startswith("refactor:"):
            return "🧹 Refactor"
        elif lower.startswith("test:"):
            return "🧪 Test"
        elif lower.startswith("doc:"):
            return "📝 Docs"
        elif lower.startswith("chore:"):
            return "⚙️ Chore"
        return "🔍 Other"

    def add_summary(self) -> "PullRequestReport":
        """Generate the branch summary for Clockify."""
        if not self.context:
            return self

        if not self.context["commits"]:
            return self

        state = self.context.get("state")
        number = self.context.get("number")
        title = self.context.get("title")
        branch_name = self.context.get("branch_name")
        url = self.context.get("url")

        if not any([state, number, title, branch_name, url]):
            return self

        status_emoji = {
            "MERGED": "✅",
            "OPEN": "🔄",
            "CLOSED": "✅",
        }.get(state.upper(), "❔")
        summary = f"{status_emoji} PR #{number} - {title}\n" f"{url}\n\n"
        summary += f"Branch: {branch_name}\n\n"

        commits = self.context["commits"]
        categories: Dict[str, List[CommitData]] = {}
        for c in commits:
            category = self.categorize_commit_message(c.message)
            categories.setdefault(category, []).append(c)

        summary += "Work Summary:\n\n"
        for category, category_commits in categories.items():
            summary += f"{category} ({len(category_commits)} commits)\n"
            for c in category_commits:
                clean_message = re.sub(
                    r"^[a-z]+:\s*", "", c.message, flags=re.I
                ).strip()
                summary += f"- {clean_message} {c.hash}\n"
            summary += "\n"

        self.context["summary"] = summary
        return self

    def add_commits(self, commits: List[CommitData]) -> "PullRequestReport":
        if self.context:
            self.context["commits"] = commits
        return self

    def add_pr(self, pr: PullRequestData) -> "PullRequestReport":
        if self.context:
            self.context["pr"] = pr
            self.context["state"] = pr.state
            self.context["number"] = pr.number
            self.context["title"] = pr.title
            self.context["branch_name"] = pr.branch_name
            self.context["url"] = pr.url
            self.context["repo_name"] = pr.repo_name
        return self

    def export_markdown(self) -> str:
        if self.context and self.context["summary"]:
            return self.context["summary"]
        return ""
