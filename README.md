# Trackify

Trackify is a powerful tool for tracking time spent on GitHub pull requests and branches. It integrates with GitHub, WakaTime, and Clockify to provide comprehensive time tracking and reporting capabilities.

## Features

- **Pull Request Tracking**: Fetch PR details and commits from GitHub
- **Time Tracking**: Calculate time spent on branches using WakaTime data
- **Time Logging**: Log time entries to Clockify with detailed descriptions
- **Summary Generation**: Create detailed PR summaries with commit categorization
- **Command Line Interface**: Easy-to-use CLI for tracking and reporting

## Installation

### Prerequisites

- Python 3.10 or higher
- GitHub account and [Personal Access Token](https://github.com/settings/tokens)
- [WakaTime](https://wakatime.com/) account and API key
- [Clockify](https://clockify.me/) account and API key

### Setup

#### Option 1: Install from PyPI (Recommended)

```bash
pip install trackify
```

Then create a `.env` file in your working directory or set environment variables:

```bash
cp .env.example .env
# Edit .env with your API keys
```

#### Option 2: Install from Source

**Quick Setup (Linux/macOS)**

```bash
git clone https://github.com/pedroifgonzalez/trackify.git
cd trackify
./setup.sh
```

This script will create a virtual environment, install dependencies, and create a `.env` file from the example. You'll just need to edit the `.env` file with your API keys.

**Manual Setup**

1. Clone the repository:

```bash
git clone https://github.com/pedroifgonzalez/trackify.git
cd trackify
```

2. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

3. Set up environment variables:

Copy the example configuration file and fill in your values:

```bash
cp .env.example .env
# Edit .env with your API keys
```

**Getting API Keys:**

- **GitHub Token**: Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens) and create a token with `repo` scope
- **WakaTime API Key**: Find it in your [WakaTime Settings](https://wakatime.com/settings/account)
- **Clockify API Key**: Generate one in [Clockify Settings > Profile Settings](https://app.clockify.me/user/settings)
- **Clockify Workspace & Project IDs**: Find these in the Clockify URL when viewing your workspace/project

## Usage

Trackify provides two main commands:

### Track Time for a Pull Request

```bash
trackify trackpr <pr_id>
```

**Example:**
```bash
trackify trackpr 123
```

This command:
1. Fetches the PR details from GitHub
2. Calculates time spent on the branch using WakaTime
3. Generates a summary of the PR with categorized commits
4. Logs the time to Clockify

### Generate PR Summary

```bash
trackify get-pr-summary <pr_id> [date]
```

**Examples:**
```bash
# Get summary for today
trackify get-pr-summary 123

# Get summary for a specific date
trackify get-pr-summary 123 2025-10-11
```

This command generates and displays a summary of the PR without logging time to Clockify.

**Note:** If you installed from source, use `python main.py` instead of `trackify`.

For more detailed instructions, see the [Quick Start Guide](docs/quickstart.md).

## Architecture

Trackify follows a modular architecture with clear separation of concerns:

### Core Components

- **Orchestrator**: Coordinates the workflow between different services
- **Code Trackers**: Interface with code repositories (e.g., GitHub)
- **Activity Trackers**: Track time spent on activities (e.g., WakaTime)
- **Time Managers**: Log time entries to time tracking services (e.g., Clockify)
- **Report Generators**: Generate summaries and reports
- **Communication Channels**: Notify messages across multiple com platforms (e.g., Slack)

### Design Patterns

- **Fluent Interface**: The Orchestrator uses a fluent interface for method chaining
- **Dependency Injection**: Services are injected into the Orchestrator
- **Interface Segregation**: Clear interfaces for each type of service

For detailed architecture diagrams, see the [architecture documentation](docs/architecture.md).

## Troubleshooting

### Common Issues

**Missing Environment Variables**
```
ValueError: Missing required environment variables: ACCESS_TOKEN, REPO_NAME
```
**Solution**: Make sure your `.env` file exists and contains all required variables. Check that you're running the command from the project directory.

**Invalid Date Format**
```
Error: Invalid date format '10-11-2025'. Please use ISO format (YYYY-MM-DD).
```
**Solution**: Use the ISO date format: `YYYY-MM-DD`, e.g., `2025-10-11`.

**GitHub API Rate Limit**
```
GitHub API rate limit exceeded
```
**Solution**: Wait for the rate limit to reset or use a GitHub token with higher limits.

**No Time Data Found**
```
ValueError: No time data found for the specified branch and project.
```
**Solution**: Ensure you have WakaTime tracking enabled for the project and branch. Check that the branch name matches exactly.

### Debug Mode

For more detailed error messages, you can set the log level:

```bash
export LOG_LEVEL=DEBUG
trackify trackpr 123
```

## Development

### Running Tests

```bash
python -m pytest
```

Tests use VCR to record and replay HTTP interactions, making them fast and reliable.

### Code Quality

The project uses several tools to maintain code quality:

- **Black**: Code formatting
- **MyPy**: Static type checking
- **Bandit**: Security linting
- **Pre-commit**: Git hooks for code quality checks

To set up pre-commit hooks:

```bash
pre-commit install
```

To run all checks manually:

```bash
black src/ tests/
mypy src/
bandit -r src/
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
