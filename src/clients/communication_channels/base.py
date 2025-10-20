from abc import ABC, abstractmethod
from typing import Any


class BaseNotifier(ABC):
    """Abstract base class for all communication channels."""

    @abstractmethod
    def notify(self, message: str, **kwargs: Any) -> None:
        """Send a notification with optional metadata."""
        pass
