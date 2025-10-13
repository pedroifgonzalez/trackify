import logging

import pytest
import typer
from freezegun import freeze_time

from src.cli.commands.pr import get_pr_summary


@pytest.mark.vcr()
def test_get_pr_summary():
    result = get_pr_summary(pr_id=592, date="2025-10-10")
    assert result
    assert result["summary"]


@freeze_time("2025-10-12")
@pytest.mark.vcr()
def test_get_pr_summary_today():
    context = get_pr_summary(pr_id=592, date=None)
    assert context["duration"] == "No duration"
    assert context["start"] == "No start"
    assert context["end"] == "No end"


@pytest.mark.vcr()
def test_get_pr_summary_invalid_date(caplog):
    caplog.set_level(logging.ERROR)
    with pytest.raises(typer.Exit) as exc_info:
        get_pr_summary(pr_id=592, date="invalid-date")
    assert exc_info.value.exit_code == 1
