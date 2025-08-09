from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment."""

    api_key: str = ""
    database_url: str = ""

    model_config = SettingsConfigDict(env_file=".env")
