import datetime
import os

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from src.clients.activity_trackers.wakatime.client import WakaClient
from src.clients.code_trackers.github.client import GitHubClient
from src.clients.time_managers.clockify.client import ClockifyClient
from src.generators.summaries.pullrequest import PullRequestReport
from src.orchestrator.main import Orchestrator
from src.utils.time import beautify_datetime, get_time_short_description
from tests.test_clockify import CLOCKIFY_API_KEY

app = typer.Typer()
console = Console()

GITHUB_ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
REPO_NAME = os.getenv("REPO_NAME")
WAKATIME_API_KEY = os.getenv("WAKATIME_API_KEY")
CLOCKIFY_API_KEY = os.getenv("CLOCKIFY_API_KEY")
CLOCKIFY_PROJECT_ID = os.getenv("CLOCKIFY_PROJECT_ID")
CLOCKIFY_WORKSPACE_ID = os.getenv("CLOCKIFY_WORKSPACE_ID")


if not any(
    [
        GITHUB_ACCESS_TOKEN,
        WAKATIME_API_KEY,
        CLOCKIFY_API_KEY,
        REPO_NAME,
        CLOCKIFY_PROJECT_ID,
        CLOCKIFY_WORKSPACE_ID,
    ]
):
    raise ValueError("Missing required environment variables.")


@app.command()
def trackpr(pr_id: int) -> None:
    """Track time spent on a pull request and log it to Clockify."""
    with console.status(f"[bold green]Processing PR #{pr_id}...", spinner="point"):
        (
            Orchestrator()
            .with_code_tracker(
                GitHubClient(
                    access_token=GITHUB_ACCESS_TOKEN,
                    repo_name=REPO_NAME,
                )
            )
            .with_activity_tracker(
                WakaClient(
                    api_key=WAKATIME_API_KEY,
                )
            )
            .with_time_manager(
                ClockifyClient(
                    api_key=CLOCKIFY_API_KEY,
                    project_id=CLOCKIFY_PROJECT_ID,
                    workspace_id=CLOCKIFY_WORKSPACE_ID,
                )
            )
            .get_pull(pr_id)
            .compute_time()
            .add_summary()
            .log_time()
        )

    console.print(
        "[bold green]✓[/bold green] [bold]Time tracking completed successfully![/bold]"
    )


@app.command()
def get_pr_summary(
    pr_id: int,
    date: str = typer.Argument(
        datetime.date.today().isoformat(),
        help="Date of the pull request. Defaults to today.",
    ),
):
    """Generate and display a summary for a GitHub pull request."""
    # Show a spinner while fetching PR data
    with console.status(f"[bold blue]Fetching PR #{pr_id} data...", spinner="dots"):
        orchestrator = Orchestrator()
        (
            orchestrator.with_code_tracker(
                GitHubClient(
                    access_token=GITHUB_ACCESS_TOKEN,
                    repo_name=REPO_NAME,
                )
            )
            .with_activity_tracker(
                WakaClient(
                    api_key=WAKATIME_API_KEY,
                )
            )
            .with_report_generator(PullRequestReport())
            .get_pull(pr_id)
            .compute_time(search_date=datetime.datetime.fromisoformat(date))
            .add_summary()
        )

    # Display the summary in a nice panel
    console.print(
        Panel.fit(
            orchestrator.context.get("summary", "No summary available"),
            title=f"[bold cyan]PR #{pr_id} Summary[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        )
    )

    duration = get_time_short_description(orchestrator.context.get("duration", 0))
    start = beautify_datetime(orchestrator.context.get("start", "No start available"))
    end = beautify_datetime(orchestrator.context.get("end", "No end available"))

    console.print(
        Panel.fit(
            f"{duration}\nStart: {start}\nEnd: {end}",
            title=f"[bold cyan]PR #{pr_id} Duration[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        )
    )

    console.print(
        "[bold green]✓[/bold green] [bold]Summary generated successfully![/bold]"
    )


if __name__ == "__main__":
    # Add a nice title to the CLI app
    console.print(Text("TRACKIFY", style="bold cyan"), justify="center")
    console.print(
        Text("GitHub PR Time Tracking Tool\n\n", style="italic"), justify="center"
    )

    app()
