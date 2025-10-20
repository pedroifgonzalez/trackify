# src/clients/communication_channels/__init__.py

import logging
from typing import Any, List

from src.clients.communication_channels.base import BaseNotifier
from src.clients.communication_channels.slack.client import SlackNotifier

logger = logging.getLogger(__name__)


class NotifierManager:
    def __init__(self) -> None:
        self.notifiers: List[BaseNotifier] = []

    def use_slack(
        self, webhook_url: str, default_channel: str = "#general"
    ) -> "NotifierManager":
        """Add Slack notifier"""
        self.notifiers.append(SlackNotifier(webhook_url, default_channel))
        return self

    def notify(self, message: str, **kwargs: Any) -> "NotifierManager":
        """Send message to all added notifiers"""
        for notifier in self.notifiers:
            try:
                notifier.notify(message, **kwargs)
            except Exception as e:
                logger.error(
                    f"[NotifierManager] Failed via {notifier.__class__.__name__}: {e}"
                )
        return self
