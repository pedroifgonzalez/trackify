from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ActivityDuration:
    start: datetime
    end: datetime
    duration: float


class IActivityTracker(ABC):
    """Interface for activity tracking services like RescueTime."""

    @abstractmethod
    def get_total_time(
        self,
        branch_name: str,
        project_name: str,
        search_date: Optional[datetime] = None,
    ) -> Optional[ActivityDuration]: ...
