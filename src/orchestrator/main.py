from github.client import GitHubClient
from wakatime.client import WakaClient
from clockify.client import ClockifyClient


def handle_pr_merge(pr_id):
    gh = GitHubClient()
    waka = WakaClient()
    clock = ClockifyClient()

    pr = gh.get_pull_request(pr_id)
    wakatime_summary = waka.get_time_summary(pr.created_at, pr.merged_at, pr.branch)
    clock.create_time_entry(pr, wakatime_summary)
