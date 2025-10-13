from unittest.mock import patch

import pytest
import typer

from src.cli.decorators import handle_errors
from src.core.exceptions import (
    ClientError,
    ConfigError,
    OrchestratorError,
    TrackifyError,
    ValidationError,
)


def test_successful_execution():
    """Test decorator allows successful function execution."""

    @handle_errors
    def successful_func(x, y):
        return x + y

    result = successful_func(2, 3)
    assert result == 5


def test_successful_execution_with_kwargs():
    """Test decorator preserves kwargs in successful execution."""

    @handle_errors
    def func_with_kwargs(a, b=10):
        return a * b

    result = func_with_kwargs(5, b=3)
    assert result == 15


@patch("src.cli.decorators.console")
@patch("src.cli.decorators.logger")
def test_trackify_error_handling(mock_logger, mock_console):
    """Test decorator catches TrackifyError and exits with code 1."""

    @handle_errors
    def raises_trackify_error():
        raise TrackifyError("Test error message")

    with pytest.raises(typer.Exit) as exc_info:
        raises_trackify_error()

    assert exc_info.value.exit_code == 1
    mock_logger.error.assert_called_once_with("Trackify error: Test error message")
    mock_console.print.assert_called_once_with(
        "[bold red]Error:[/bold red] Test error message"
    )


@patch("src.cli.decorators.console")
@patch("src.cli.decorators.logger")
def test_config_error_handling(mock_logger, mock_console):
    """Test decorator catches ConfigError (subclass of TrackifyError)."""

    @handle_errors
    def raises_config_error():
        raise ConfigError("Invalid configuration")

    with pytest.raises(typer.Exit) as exc_info:
        raises_config_error()

    assert exc_info.value.exit_code == 1
    mock_logger.error.assert_called_once_with("Trackify error: Invalid configuration")
    mock_console.print.assert_called_once_with(
        "[bold red]Error:[/bold red] Invalid configuration"
    )


@patch("src.cli.decorators.console")
@patch("src.cli.decorators.logger")
def test_client_error_handling(mock_logger, mock_console):
    """Test decorator catches ClientError (subclass of TrackifyError)."""

    @handle_errors
    def raises_client_error():
        raise ClientError("API request failed")

    with pytest.raises(typer.Exit) as exc_info:
        raises_client_error()

    assert exc_info.value.exit_code == 1
    mock_logger.error.assert_called_once_with("Trackify error: API request failed")


@patch("src.cli.decorators.console")
@patch("src.cli.decorators.logger")
def test_orchestrator_error_handling(mock_logger, mock_console):
    """Test decorator catches OrchestratorError (subclass of TrackifyError)."""

    @handle_errors
    def raises_orchestrator_error():
        raise OrchestratorError("Orchestration step failed")

    with pytest.raises(typer.Exit) as exc_info:
        raises_orchestrator_error()

    assert exc_info.value.exit_code == 1


@patch("src.cli.decorators.console")
@patch("src.cli.decorators.logger")
def test_validation_error_handling(mock_logger, mock_console):
    """Test decorator catches ValidationError (subclass of TrackifyError)."""

    @handle_errors
    def raises_validation_error():
        raise ValidationError("Invalid input")

    with pytest.raises(typer.Exit) as exc_info:
        raises_validation_error()

    assert exc_info.value.exit_code == 1


@patch("src.cli.decorators.console")
@patch("src.cli.decorators.logger")
def test_generic_exception_handling(mock_logger, mock_console):
    """Test decorator catches generic exceptions and exits with code 1."""

    @handle_errors
    def raises_generic_error():
        raise ValueError("Unexpected error")

    with pytest.raises(typer.Exit) as exc_info:
        raises_generic_error()

    assert exc_info.value.exit_code == 1
    mock_logger.exception.assert_called_once_with("Unexpected error occurred.")
    mock_console.print.assert_called_once_with(
        "[bold red]Unexpected error:[/bold red] Something went wrong. "
        "Use --debug for more info."
    )


@patch("src.cli.decorators.console")
@patch("src.cli.decorators.logger")
def test_runtime_error_handling(mock_logger, mock_console):
    """Test decorator catches RuntimeError."""

    @handle_errors
    def raises_runtime_error():
        raise RuntimeError("Runtime issue")

    with pytest.raises(typer.Exit) as exc_info:
        raises_runtime_error()

    assert exc_info.value.exit_code == 1
    mock_logger.exception.assert_called_once()


def test_preserves_function_metadata():
    """Test decorator preserves original function metadata."""

    @handle_errors
    def documented_function():
        """This is a documented function."""
        pass

    assert documented_function.__name__ == "documented_function"
    assert documented_function.__doc__ == "This is a documented function."


@patch("src.cli.decorators.console")
@patch("src.cli.decorators.logger")
def test_with_return_value(mock_logger, mock_console):
    """Test decorator preserves return values."""

    @handle_errors
    def returns_dict():
        return {"status": "success", "data": [1, 2, 3]}

    result = returns_dict()
    assert result == {"status": "success", "data": [1, 2, 3]}


@patch("src.cli.decorators.console")
@patch("src.cli.decorators.logger")
def test_with_args_and_kwargs(mock_logger, mock_console):
    """Test decorator works with both args and kwargs."""

    @handle_errors
    def complex_function(a, b, c=None, d=None):
        return {"a": a, "b": b, "c": c, "d": d}

    result = complex_function(1, 2, c=3, d=4)
    assert result == {"a": 1, "b": 2, "c": 3, "d": 4}


@patch("src.cli.decorators.console")
@patch("src.cli.decorators.logger")
def test_error_message_formatting(mock_logger, mock_console):
    """Test error messages are formatted correctly."""

    @handle_errors
    def raises_with_special_chars():
        raise TrackifyError("Error with 'quotes' and \"double quotes\"")

    with pytest.raises(typer.Exit):
        raises_with_special_chars()

    mock_console.print.assert_called_once_with(
        "[bold red]Error:[/bold red] Error with 'quotes' and \"double quotes\""
    )
