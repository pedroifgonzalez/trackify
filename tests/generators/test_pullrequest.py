import pytest

from src.generators.summaries.pullrequest import PullRequestReport
from src.shared.dtos import PullRequestData


@pytest.mark.parametrize(
    "message, category",
    [
        ("feat: Add feature", "✨ Feature"),
        ("fix: Fix bug", "🐛 Fix"),
        ("refactor: Refactor code", "🧹 Refactor"),
        ("test: Add tests", "🧪 Test"),
        ("doc: Add documentation", "📝 Docs"),
        ("chore: Update dependencies", "⚙️ Chore"),
        ("other: Other", "🔍 Other"),
    ],
)
def test_categorize_commit_message(message, category):
    pull_request_report = PullRequestReport()
    assert pull_request_report.categorize_commit_message(message) == category


def test_export_markdown_no_summary():
    pull_request_report = PullRequestReport()
    assert pull_request_report.export_markdown() == ""


def test_add_summary_no_commits():
    pull_request_report = PullRequestReport(
        data=PullRequestData(
            number=1,
            title="Test Pull Request",
            branch_name="test/pull-request",
            state="open",
            url="test-url",
        )
    )
    pull_request_report.add_summary()
    assert pull_request_report.context.get("summary") == None
