# Trackify Quick Start Guide

This guide will help you get started with Trackify quickly.

## Prerequisites

Before you begin, make sure you have:

1. A GitHub account and personal access token with repo scope
2. A WakaTime account and API key
3. A Clockify account with API key, workspace ID, and project ID
4. Python 3.13 or higher installed

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/trackify.git
cd trackify
```

2. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

## Configuration

Create a `.env` file in the project root with the following content:

```
ACCESS_TOKEN=your-github-token
REPO_NAME=owner/repo
WAKATIME_API_KEY=your-wakatime-api-key
CLOCKIFY_API_KEY=your-clockify-api-key
CLOCKIFY_WORKSPACE_ID=your-clockify-workspace-id
CLOCKIFY_PROJECT_ID=your-clockify-project-id
```

## Basic Usage

### Track time for a pull request

```bash
python main.py trackpr 123  # Replace 123 with your PR number
```

This will:
1. Fetch the PR details from GitHub
2. Calculate time spent on the branch using WakaTime
3. Generate a summary with categorized commits
4. Log the time to Clockify

### Generate a PR summary without logging time

```bash
python main.py get-pr-summary 123  # Replace 123 with your PR number
```

## Troubleshooting

### No time data found

If you get an error like "No time data found for the specified branch and project":

1. Make sure your WakaTime is properly configured and tracking time for the repository
2. Check that the branch name in WakaTime matches the branch name in GitHub
3. Verify that the project name in WakaTime matches the repository name

### API Authentication Issues

If you encounter authentication errors:

1. Verify that your API keys are correct and have the necessary permissions
2. Check that your environment variables are properly set
3. For GitHub, ensure your token has the 'repo' scope

## Next Steps

- Check out the [architecture documentation](architecture.md) to understand how Trackify works
- Explore the code to see how you can extend or customize Trackify for your needs
