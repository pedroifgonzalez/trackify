from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    GITHUB_ACCESS_TOKEN: str
    REPO_NAME: str
    WAKATIME_API_KEY: str
    CLOCKIFY_API_KEY: str
    CLOCKIFY_PROJECT_ID: str
    CLOCKIFY_WORKSPACE_ID: str


config = Config()
