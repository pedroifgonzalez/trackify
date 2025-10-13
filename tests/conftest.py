import os
from pathlib import Path

import pytest

# Set test environment file BEFORE importing config
os.environ["TRACKIFY_ENV_FILE"] = str(Path(__file__).parent.parent / ".env.test")


@pytest.fixture(scope="session", autouse=True)
def test_config():
    """Load test configuration from .env.test and inject into config module."""
    # Import after setting the environment variable
    import src.cli.commands.config as config_module
    from src.cli.commands.config import Config

    test_env_path = Path(__file__).parent.parent / ".env.test"

    # Create a test config instance that loads from .env.test
    test_config = Config(_env_file=test_env_path)

    # Replace the global config and cached config with test config
    config_module.config = test_config
    config_module._config = test_config  # Also update the cached instance

    return test_config


def scrub_api_keys(request):
    """Filter sensitive information from VCR cassettes."""
    # Replace GitHub token in Authorization header
    if "Authorization" in request.headers:
        if "token " in request.headers["Authorization"]:
            request.headers["Authorization"] = "token GITHUB_TOKEN_PLACEHOLDER"

    # Replace Clockify API key
    if "X-Api-Key" in request.headers:
        request.headers["X-Api-Key"] = "CLOCKIFY_API_KEY_PLACEHOLDER"

    # Replace WakaTime API key
    if "Authorization" in request.headers:
        if "Basic " in request.headers["Authorization"]:
            request.headers["Authorization"] = "Basic WAKATIME_API_KEY_PLACEHOLDER"

    return request


@pytest.fixture(autouse=True, scope="module")
def vcr_config():
    """VCR configuration for pytest-vcr."""
    return {
        "filter_headers": ["Authorization", "X-Api-Key"],
        "before_record_request": scrub_api_keys,
    }
