import pytest

from src.cli.commands.pr import trackpr


@pytest.mark.vcr()
def test_trackpr():
    context = trackpr(pr_id=592, date="2025-10-10")
    assert context
