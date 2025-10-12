import datetime
import logging

import typer
from rich.console import Console

from src.cli.commands.config import config
from src.clients.activity_trackers.wakatime.client import WakaClient
from src.clients.code_trackers.github.client import GitHubClient
from src.clients.time_managers.clockify.client import ClockifyClient
from src.core.orchestrator import Orchestrator
from src.generators.summaries.pullrequest import PullRequestReport
from src.utils.time import beautify_datetime, get_time_short_description

console = Console()
pr_app = typer.Typer(help="Handle GitHub PRs and summaries.")


logger = logging.getLogger("trackify.pr")


@pr_app.command()
def trackpr(pr_id: int) -> None:
    """Track time spent on a pull request and log it to Clockify."""
    logger.info(f"Starting time tracking for PR #{pr_id}")
    with console.status(f"[bold green]Processing PR #{pr_id}...", spinner="point"):
        (
            Orchestrator()
            .with_code_tracker(
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


@pr_app.command()
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
                    access_token=config.GITHUB_ACCESS_TOKEN,
                    repo_name=config.REPO_NAME,
                )
            )
            .with_activity_tracker(
                WakaClient(
                    api_key=config.WAKATIME_API_KEY,
                )
            )
            .with_report_generator(PullRequestReport())
            .get_pull(pr_id)
            .compute_time(search_date=search_date)
            .add_summary()
        )

    # Display the summary in a nice panel
    console.print(
        typer.Panel.fit(
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
        typer.Panel.fit(
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
