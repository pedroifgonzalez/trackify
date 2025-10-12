import datetime
import logging
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.cli.commands.config import config
from src.cli.decorators import handle_errors
from src.clients.activity_trackers.wakatime.client import WakaClient
from src.clients.code_trackers.github.client import GitHubClient
from src.clients.time_managers.clockify.client import ClockifyClient
from src.core.orchestrator import Orchestrator
from src.generators.summaries.pullrequest import PullRequestReport

console = Console()
pr_app = typer.Typer(help="Handle GitHub PRs and summaries.")


logger = logging.getLogger("trackify.pr")


@pr_app.command()
@handle_errors
def trackpr(pr_id: int) -> dict:
    """Track time spent on a pull request and log it to Clockify."""
    logger.info(f"Starting time tracking for PR #{pr_id}")
    with console.status(f"[bold green]Processing PR #{pr_id}...", spinner="point"):
        orchestrator = Orchestrator()
        (
            orchestrator.with_code_tracker(
                GitHubClient(
                    access_token=config.GITHUB_ACCESS_TOKEN,
                    repo_name=config.REPO_NAME,
                )
            )
            .with_activity_tracker(
                WakaClient(
                    api_key=config.WAKATIME_API_KEY,
                )
            )
            .with_time_manager(
                ClockifyClient(
                    api_key=config.CLOCKIFY_API_KEY,
                    project_id=config.CLOCKIFY_PROJECT_ID,
                    workspace_id=config.CLOCKIFY_WORKSPACE_ID,
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
    return orchestrator.context


@pr_app.command()
@handle_errors
def get_pr_summary(
    pr_id: int,
    date: str = typer.Argument(
        None,
        help="Date of the pull request in ISO format (YYYY-MM-DD). Defaults to today.",
    ),
) -> dict:
    """Generate and display a summary for a GitHub pull request."""
    logger.info(f"Generating summary for PR #{pr_id}")

    # The date is already validated and parsed by the decorator
    search_date = (
        datetime.datetime.fromisoformat(date) if date else datetime.datetime.now()
    )

    orchestrator = (
        Orchestrator()
        .stage(
            "Setting code tracker",
            "with_code_tracker",
            GitHubClient(
                access_token=config.GITHUB_ACCESS_TOKEN,
                repo_name=config.REPO_NAME,
            ),
        )
        .stage(
            "Setting activity tracker",
            "with_activity_tracker",
            WakaClient(
                api_key=config.WAKATIME_API_KEY,
            ),
        )
        .stage("Setting report generator", "with_report_generator", PullRequestReport())
        .stage("Fetching PR", "get_pull", pr_id)
        .stage("Computing time", "compute_time", search_date=search_date)
        .stage("Generating summary", "add_summary")
        .stage("Beautifying context", "beautify_context")
    )

    # Prepare panels
    summary_panel = Panel(
        orchestrator.context.get("summary", "No summary available"),
        title=f"[bold cyan]PR #{pr_id} Summary[/bold cyan]",
        border_style="cyan",
        padding=(1, 2),
    )

    duration_panel = Panel(
        f"{orchestrator.context.get('duration', 'No duration')}\nStart: {orchestrator.context.get('start', 'No start available')}\nEnd: {orchestrator.context.get('end', 'No end available')}",
        title=f"[bold cyan]PR #{pr_id} Duration[/bold cyan]",
        border_style="cyan",
        padding=(1, 2),
    )

    # Create a table to display panels side by side
    layout = Table.grid(expand=True)
    layout.add_column(ratio=3)
    layout.add_column(ratio=1)
    layout.add_row(summary_panel, duration_panel)

    console.print(layout)
    console.print(
        "[bold green]✓[/bold green] [bold]Summary generated successfully![/bold]",
        justify="center",
    )

    return orchestrator.context
