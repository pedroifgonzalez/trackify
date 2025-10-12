import datetime
import logging
import os
import sys

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

console = Console()

# Configure logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("trackify")

GITHUB_ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "")
REPO_NAME = os.getenv("REPO_NAME", "")
WAKATIME_API_KEY = os.getenv("WAKATIME_API_KEY", "")
CLOCKIFY_API_KEY = os.getenv("CLOCKIFY_API_KEY", "")
CLOCKIFY_PROJECT_ID = os.getenv("CLOCKIFY_PROJECT_ID", "")
CLOCKIFY_WORKSPACE_ID = os.getenv("CLOCKIFY_WORKSPACE_ID", "")


# Validate required environment variables
missing_vars = []
if not GITHUB_ACCESS_TOKEN:
    missing_vars.append("ACCESS_TOKEN")
if not WAKATIME_API_KEY:
    missing_vars.append("WAKATIME_API_KEY")
if not CLOCKIFY_API_KEY:
    missing_vars.append("CLOCKIFY_API_KEY")
if not REPO_NAME:
    missing_vars.append("REPO_NAME")
if not CLOCKIFY_PROJECT_ID:
    missing_vars.append("CLOCKIFY_PROJECT_ID")
if not CLOCKIFY_WORKSPACE_ID:
    missing_vars.append("CLOCKIFY_WORKSPACE_ID")

if missing_vars:
    error_msg = (
        f"Missing required environment variables: {', '.join(missing_vars)}. "
        "Please set them in your .env file or environment."
    )
    logger.error(error_msg)
    raise ValueError(error_msg)


app = typer.Typer()


@app.command()
def trackpr(pr_id: int) -> None:
    """Track time spent on a pull request and log it to Clockify."""
    logger.info(f"Starting time tracking for PR #{pr_id}")
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

    logger.info(f"Time tracking completed successfully for PR #{pr_id}")
    console.print(
        "[bold green]✓[/bold green] [bold]Time tracking completed successfully![/bold]"
    )


@app.command()
def get_pr_summary(
    pr_id: int,
    date: str = typer.Argument(
        None,
        help="Date of the pull request in ISO format (YYYY-MM-DD). Defaults to today.",
    ),
) -> None:
    """Generate and display a summary for a GitHub pull request."""
    logger.info(f"Generating summary for PR #{pr_id}")

    # Validate date format
    try:
        # Use today's date if not provided
        if not date:
            date = datetime.date.today().isoformat()
        search_date = datetime.datetime.fromisoformat(date)
        logger.debug(f"Using search date: {search_date}")
    except ValueError:
        logger.error(f"Invalid date format: {date}")
        console.print(
            f"[bold red]Error:[/bold red] Invalid date format '{date}'. "
            "Please use ISO format (YYYY-MM-DD)."
        )
        raise typer.Exit(code=1)

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
            .compute_time(search_date=search_date)
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
    logger.info(f"Summary generated successfully for PR #{pr_id}")
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
