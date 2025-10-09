import re
from typing import Dict, List, Optional

from src.github.dtos import CommitData, PullRequestData

from .base import FluentBase


class PullRequestReport(FluentBase):
    """Enriched PullRequestDTO with summarization and analytics."""

    def __init__(
        self,
        data: Optional[PullRequestData],
    ):
        self.data = data

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
        if not self.data:
            return self

        if not self.data.commits:
            return self

        summary = f"# Branch: {self.data.branch_name}\n\n"
        commits = self.data.commits
        status_emoji = {
            "MERGED": "✅",
            "OPEN": "🔄",
            "CLOSED": "❌",
        }.get(self.data.state.upper(), "❔")
        summary += (
            f"**Pull Request**: {status_emoji} PR #{self.data.number} - {self.data.title}\n"
            f"**PR URL**: {self.data.url}\n\n"
        )
        pr_numbers = {
            match for c in commits for match in re.findall(r"#(\d+)", c.message)
        }
        if pr_numbers:
            summary += (
                f"**Related PRs**: #{', #'.join(sorted(pr_numbers, key=int))}\n\n"
            )
        summary += f"**Total Commits**: {len(commits)}\n"

        authors = sorted(set(c.author for c in commits))
        if len(authors) == 1:
            summary += f"**Developer**: {authors[0]}\n\n"
        else:
            summary += f"**Developers**: {', '.join(authors)}\n\n"

        categories: Dict[str, List[CommitData]] = {}
        for c in commits:
            category = self.categorize_commit_message(c.message)
            categories.setdefault(category, []).append(c)

        summary += "## Work Summary:\n\n"
        for category, category_commits in categories.items():
            summary += f"### {category} ({len(category_commits)} commits)\n"
            for c in category_commits:
                clean_message = re.sub(
                    r"^[a-z]+:\s*", "", c.message, flags=re.I
                ).strip()
                summary += f"- {clean_message} `{c.hash}`\n"
            summary += "\n"

        if len(commits) <= 10:
            summary += "## Commit History:\n\n"
            for c in commits:
                emoji = self.categorize_commit_message(c.message).split()[0]
                summary += f"- {emoji} **{c.date}**: {c.message} `{c.hash}`\n"

        self.data.summary = summary
        return self

    def add_commits(self, commits: List[CommitData]) -> "PullRequestReport":
        if self.data:
            self.data.commits = commits
        return self

    def export_markdown(self) -> str:
        if self.data and self.data.summary:
            return self.data.summary
        return ""
