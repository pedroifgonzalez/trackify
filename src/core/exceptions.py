"""Custom exception hierarchy for Trackify."""


class TrackifyError(Exception):
    """Base exception for Trackify."""


class ConfigError(TrackifyError):
    """Raised when configuration or environment is invalid."""


class ClientError(TrackifyError):
    """Raised when a client (GitHub, WakaTime, etc.) fails."""


class OrchestratorError(TrackifyError):
    """Raised when an orchestration step fails."""


class ValidationError(TrackifyError):
    """Raised for invalid CLI or user input."""
