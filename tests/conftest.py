import os
import pytest
import vcr


def scrub_api_keys(request):
    """Filter sensitive information from VCR cassettes."""
    # Replace GitHub token in Authorization header
    if "Authorization" in request.headers:
        if "token " in request.headers["Authorization"]:
            request.headers["Authorization"] = "token GITHUB_TOKEN_PLACEHOLDER"

    # Replace Clockify API key
    if "X-Api-Key" in request.headers:
        request.headers["X-Api-Key"] = "CLOCKIFY_API_KEY_PLACEHOLDER"

    return request


# Configure VCR with custom settings
trackify_vcr = vcr.VCR(
    filter_headers=["Authorization", "X-Api-Key"],
    before_record_request=scrub_api_keys,
    record_mode="once",
)


@pytest.fixture
def vcr_config():
    """VCR configuration for pytest-vcr."""
    return {
        "filter_headers": ["Authorization", "X-Api-Key"],
        "before_record_request": scrub_api_keys,
    }
