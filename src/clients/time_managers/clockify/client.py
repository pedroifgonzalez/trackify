import datetime
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
