import datetime
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests

from src.clients.time_managers.base import ITimeManager, TimeEntry
from src.core.exceptions import ClientError


class ClockifyClient(ITimeManager):
    # Define a constant for date format
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def __init__(self, api_key: str, workspace_id: str, project_id: str) -> None:
        """Initialize the Clockify client.

        Args:
            api_key (str): The API key to authenticate with Clockify.
            workspace_id (str): The ID of the workspace.
            project_id (str): The ID of the project.
        """
        self.api_key = api_key
        self.workspace_id = workspace_id
        self.project_id = project_id
        self.api_base_url = "https://api.clockify.me/api/v1/"

    def create_time_entry(
        self, description: str, start: datetime.datetime, end: datetime.datetime
    ) -> TimeEntry:
        """Create a time entry in Clockify

        Args:
            description (str): Description of the time entry
            start (datetime.datetime): Start date of the time entry
            end (datetime.datetime): End date of the time entry

        Returns:
            TimeEntry: Time entry created in Clockify
        """
        url = f"{self.api_base_url}workspaces/{self.workspace_id}/time-entries"
        request_data = {
            "billable": True,
            "description": description,
            "start": start.strftime(self.DATE_FORMAT),
            "end": end.strftime(self.DATE_FORMAT),
            "projectId": self.project_id,
        }
        response = requests.post(
            url,
            headers={"X-Api-Key": self.api_key},
            json=request_data,
            timeout=10,  # Add timeout to prevent hanging requests
        )
        if response.status_code != 201:
            raise ClientError(f"Failed to create time entry: {response.status_code}")
        response_data: Dict[str, Any] = response.json()
        return TimeEntry(
            billable=bool(response_data["billable"]),
            description=str(response_data["description"]),
            project_id=str(response_data["projectId"]),
            workspace_id=str(response_data["workspaceId"]),
        )

    def get_time_entries(
        self,
        project_name: str,
        branch_name: str,
        search_date: Optional[datetime.datetime] = None,
    ) -> List[Dict]:
        """Get time entries for a specific project and branch.

        Args:
            project_name (str): The name of the project.
            branch_name (str): The name of the branch.
            search_date (Optional[datetime.datetime], optional): The date to search for time entries. Defaults to None.

        Returns:
            List[Dict]: A list of time entries.
        """
        url = f"{self.api_base_url}workspaces/{self.workspace_id}/time-entries"

        # Set up query parameters
        params = {}
        if search_date:
            # Format date for Clockify API
            start_date = search_date.replace(hour=0, minute=0, second=0).strftime(
                self.DATE_FORMAT
            )
            end_date = search_date.replace(hour=23, minute=59, second=59).strftime(
                self.DATE_FORMAT
            )
            params["start"] = start_date
            params["end"] = end_date

        # Add project filter
        params["project"] = self.project_id

        response = requests.get(
            url,
            headers={"X-Api-Key": self.api_key},
            params=params,
            timeout=10,
        )

        if response.status_code != 200:
            raise ClientError(f"Failed to get time entries: {response.status_code}")

        entries = response.json()

        # Filter entries by branch name in description
        branch_entries = []
        for entry in entries:
            if branch_name.lower() in entry.get("description", "").lower():
                branch_entries.append(entry)

        return branch_entries

    def compute_total_time(
        self,
        project_name: str,
        branch_name: str,
        search_date: Optional[datetime.datetime] = None,
    ) -> float:
        """Compute the total time spent on a project and branch.

        Args:
            project_name (str): The name of the project.
            branch_name (str): The name of the branch.
            search_date (Optional[datetime.datetime], optional): The date to search for time entries. Defaults to None.

        Returns:
            float: The total time spent in hours.
        """
        entries = self.get_time_entries(project_name, branch_name, search_date)

        total_seconds = 0.0
        for entry in entries:
            start_time = datetime.datetime.fromisoformat(
                entry.get("timeInterval", {}).get("start").replace("Z", "+00:00")
            )
            end_time = datetime.datetime.fromisoformat(
                entry.get("timeInterval", {}).get("end").replace("Z", "+00:00")
            )
            duration = (end_time - start_time).total_seconds()
            total_seconds += duration

        # Convert seconds to hours
        return total_seconds / 3600.0

    def add_time_entry(
        self,
        project_name: str,
        branch_name: str,
        description: str,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
    ) -> Dict:
        """Add a time entry for a project and branch.

        Args:
            project_name (str): The name of the project.
            branch_name (str): The name of the branch.
            description (str): The description of the time entry.
            start_time (datetime.datetime): The start time of the entry.
            end_time (datetime.datetime): The end time of the entry.

        Returns:
            Dict: The created time entry.
        """
        # Format description to include branch name
        full_description = f"[{branch_name}] {description}"

        entry = self.create_time_entry(full_description, start_time, end_time)

        # Convert to dictionary format
        return {
            "description": entry.description,
            "billable": entry.billable,
            "projectId": entry.project_id,
            "workspaceId": entry.workspace_id,
            "start": start_time.strftime(self.DATE_FORMAT),
            "end": end_time.strftime(self.DATE_FORMAT),
        }
