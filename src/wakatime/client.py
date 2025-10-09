from dataclasses import dataclass
from datetime import datetime
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

    def _authenticate(self):
        """Check that the provided API key works."""
        headers = {"Authorization": f"Basic {self.api_key}"}
        resp = requests.get(f"{self.api_base_url}users/current", headers=headers)
        if resp.status_code != 200:
            print(f"Authentication failed: {resp.status_code} - {resp.text}")
            return None
        print("✅ Authenticated successfully.")
        return True

    def get_total_time(self, branch_name: str):
        """Get total time spent on a specific branch today."""
        headers = {"Authorization": f"Basic {self.api_key}"}
        # Format branches as a comma-separated list as required by the API
        params = {
            "date": datetime.today().strftime("%Y-%m-%d"),
            "branches": branch_name,  # API expects comma-separated list for multiple branches
        }

        resp = requests.get(
            f"{self.api_base_url}users/current/durations",
            headers=headers,
            params=params,
        )

        if resp.status_code != 200:
            print(f"Error getting durations: {resp.status_code} - {resp.text}")
            return None

        data = resp.json()

        # Debug information
        print(f"API Response for branch '{branch_name}':")
        print(f"  - Data entries: {len(data.get('data', []))}")
        print(f"  - URL: {resp.url}")

        # Handle empty data case
        if not data.get("data"):
            print(f"No duration data found for branch: {branch_name}")
            return WakaTotalDuration(
                start=datetime.now(),
                end=datetime.now(),
                duration=0,
            )

        durations = [item["duration"] for item in data.get("data", [])]
        total_duration = sum(durations)

        # Print found durations for debugging
        print(
            f"  - Found {len(durations)} duration entries totaling {total_duration} seconds"
        )

        return WakaTotalDuration(
            start=datetime.fromisoformat(data["start"]),
            end=datetime.fromisoformat(data["end"]),
            duration=total_duration,
        )
