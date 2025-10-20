import pytest

from src.cli.commands.config import config as cfg
from src.clients.communication_channels.slack.client import SlackNotifier


@pytest.mark.vcr
def test_send_message():
    notifier = SlackNotifier(
        bot_token=cfg.SLACK_BOT_TOKEN, user_token=cfg.SLACK_USER_TOKEN
    )
    notifier.notify("Hello world from trackify!")


@pytest.mark.vcr
def test_send_message_as_user():
    notifier = SlackNotifier(
        bot_token=cfg.SLACK_BOT_TOKEN, user_token=cfg.SLACK_USER_TOKEN
    )
    notifier.notify("Hello world from me!", as_user=True)
