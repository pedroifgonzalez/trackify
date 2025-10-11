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

- Python 3.13 or higher
- GitHub account and access token
- WakaTime account and API key
- Clockify account and API key

### Setup

#### Quick Setup (Linux/macOS)

```bash
git clone https://github.com/yourusername/trackify.git
cd trackify
./setup.sh
```

This script will create a virtual environment, install dependencies, and create a `.env` file from the example. You'll just need to edit the `.env` file with your API keys.

#### Manual Setup

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

3. Set up environment variables:

You can either set environment variables directly:

```bash
export ACCESS_TOKEN="your-github-token"
export REPO_NAME="owner/repo"
export WAKATIME_API_KEY="your-wakatime-api-key"
export CLOCKIFY_API_KEY="your-clockify-api-key"
export CLOCKIFY_WORKSPACE_ID="your-clockify-workspace-id"
export CLOCKIFY_PROJECT_ID="your-clockify-project-id"
```

On Windows, use `set` instead of `export`.

Alternatively, copy the example configuration file and fill in your values:

```bash
cp .env.example .env
# Edit .env with your values
```

## Usage

Trackify provides two main commands:

### Track Time for a Pull Request

```bash
python main.py trackpr <pr_id>
```

This command:
1. Fetches the PR details from GitHub
2. Calculates time spent on the branch using WakaTime
3. Generates a summary of the PR with categorized commits
4. Logs the time to Clockify

### Generate PR Summary

```bash
python main.py get-pr-summary <pr_id>
```

This command generates and displays a summary of the PR without logging time to Clockify.

For more detailed instructions, see the [Quick Start Guide](docs/quickstart.md).

## Architecture

Trackify follows a modular architecture with clear separation of concerns:

### Core Components

- **Orchestrator**: Coordinates the workflow between different services
- **Code Trackers**: Interface with code repositories (e.g., GitHub)
- **Activity Trackers**: Track time spent on activities (e.g., WakaTime)
- **Time Managers**: Log time entries to time tracking services (e.g., Clockify)
- **Report Generators**: Generate summaries and reports

### Design Patterns

- **Fluent Interface**: The Orchestrator uses a fluent interface for method chaining
- **Dependency Injection**: Services are injected into the Orchestrator
- **Interface Segregation**: Clear interfaces for each type of service

For detailed architecture diagrams, see the [architecture documentation](docs/architecture.md).

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

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
