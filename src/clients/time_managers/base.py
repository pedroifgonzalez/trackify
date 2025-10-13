from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TimeEntry:
    description: str
    billable: bool
    project_id: str
    workspace_id: str


class ITimeManager(ABC):
    """Interface for time tracking services like Clockify."""

    @abstractmethod
    def create_time_entry(
        self, description: str, start: datetime, end: datetime
    ) -> TimeEntry: ...
