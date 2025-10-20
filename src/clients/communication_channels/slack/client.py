from typing import Any

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from src.clients.communication_channels.base import BaseNotifier


class SlackNotifier(BaseNotifier):
    def __init__(
        self, bot_token: str, user_token: str, default_channel: str = "#general"
    ) -> None:
        self.bot_client = WebClient(token=bot_token)
        self.user_client = WebClient(token=user_token)
        self.default_channel = default_channel

    def notify(self, message: str, **kwargs: Any) -> None:
        try:
            if kwargs.get("as_user", False):
                self.user_client.chat_postMessage(
                    channel=kwargs.get("channel", self.default_channel),
                    text=message,
                )
            else:
                self.bot_client.chat_postMessage(
                    channel=kwargs.get("channel", self.default_channel),
                    text=message,
                )
        except SlackApiError as e:
            raise ValueError(f"Slack notification failed: {e.response['error']}")
