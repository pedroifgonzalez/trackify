from dataclasses import dataclass
import datetime
import requests


@dataclass
class ClockifyTimeEntry:
    description: str
    billable: bool
    projectId: str
    workspaceId: str


class ClockifyClient:
    def __init__(self, api_key, workspace_id, project_id):
        self.api_key = api_key
        self.workspace_id = workspace_id
        self.project_id = project_id
        self.api_base_url = "https://api.clockify.me/api/v1/"

    def create_time_entry(
        self, description: str, start: datetime.datetime, end: datetime.datetime
    ) -> ClockifyTimeEntry:
        """Create a time entry in Clockify

        Args:
            description (str): Description of the time entry
            start (datetime.datetime): Start date of the time entry
            end (datetime.datetime): End date of the time entry

        Returns:
            ClockifyTimeEntry: Time entry created in Clockify
        """
        url = f"{self.api_base_url}workspaces/{self.workspace_id}/time-entries"
        data = {
            "billable": True,
            "description": description,
            "start": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "end": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "projectId": self.project_id,
        }
        response = requests.post(
            url,
            headers={"X-Api-Key": self.api_key},
            json=data,
        )
        if response.status_code != 201:
            print(response.json())
            raise Exception("Failed to create time entry")
        data = response.json()
        return ClockifyTimeEntry(
            billable=data["billable"],
            description=data["description"],
            projectId=data["projectId"],
            workspaceId=data["workspaceId"],
        )
