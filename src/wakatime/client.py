from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

import requests


@dataclass
class WakaTotalDuration:
    start: datetime
    end: datetime
    duration: float


class WakaClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_base_url = "https://wakatime.com/api/v1/"

    def _authenticate(self) -> bool:
        """Check that the provided API key works."""
        headers = {"Authorization": f"Basic {self.api_key}"}
        resp = requests.get(
            f"{self.api_base_url}users/current",
            headers=headers,
            timeout=10,  # Add timeout to prevent hanging requests
        )
        if resp.status_code != 200:
            return False
        return True

    def get_total_time(
        self, branch_name: str, project: str, search_date: Optional[date] = None
    ) -> Optional[WakaTotalDuration]:
        """Get total time spent on a specific branch today.

        Args:
            branch_name (str): Branch name
            project (str): Project name
            search_date (Optional[date], optional): Date to search for. Defaults to None.

        Returns:
            WakaTotalDuration: Total time spent on the branch
        """
        headers = {"Authorization": f"Basic {self.api_key}"}
        params = {
            "date": (
                date.today().strftime("%Y-%m-%d")
                if search_date is None
                else search_date.strftime("%Y-%m-%d")
            ),
            "branches": branch_name,
            "project": project,
        }

        resp = requests.get(
            f"{self.api_base_url}users/current/durations",
            headers=headers,
            params=params,
            timeout=10,  # Add timeout to prevent hanging requests
        )

        if resp.status_code != 200 or not resp.json().get("data"):
            return None

        data = resp.json()
        durations = [item["duration"] for item in data.get("data", [])]
        total_duration = sum(durations)
        return WakaTotalDuration(
            start=datetime.fromisoformat(data["start"]),
            end=datetime.fromisoformat(data["end"]),
            duration=total_duration,
        )
