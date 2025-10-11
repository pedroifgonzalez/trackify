from datetime import date, datetime
from typing import Optional

import requests

from src.clients.activity_trackers.base import ActivityDuration, IActivityTracker


class WakaClient(IActivityTracker):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_base_url = "https://wakatime.com/api/v1/"

    def get_total_time(
        self,
        branch_name: str,
        project_name: str,
        search_date: Optional[date] = None,
        timezone: Optional[str] = "America/Havana",
    ) -> Optional[ActivityDuration]:
        """Get total time spent on a specific branch today.

        Args:
            branch_name (str): Branch name
            project_name (str): Project name
            search_date (Optional[date], optional): Date to search for. Defaults to None.

        Returns:
            ActivityDuration: Total time spent on the branch
        """
        headers = {"Authorization": f"Basic {self.api_key}"}
        params = {
            "date": (
                date.today().strftime("%Y-%m-%d")
                if search_date is None
                else search_date.strftime("%Y-%m-%d")
            ),
            "branches": branch_name,
            "project": project_name,
            "timezone": timezone,
        }

        resp = requests.get(
            f"{self.api_base_url}users/current/durations",
            headers=headers,
            params=params,
            timeout=10,
        )

        if resp.status_code != 200 or not resp.json().get("data"):
            return None

        response_data = resp.json()
        heartbeats = list(response_data.get("data", []))
        starts = [heartbeat.get("time") for heartbeat in heartbeats]
        sorted_starts = sorted(starts)
        start = sorted_starts[0]
        durations = [item["duration"] for item in heartbeats]
        total_duration = sum(durations)
        end = start + total_duration

        return ActivityDuration(
            start=datetime.fromtimestamp(start),
            end=datetime.fromtimestamp(end),
            duration=total_duration,
        )
