from __future__ import annotations

from typing import Dict

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_env: str = Field("development", alias="APP_ENV")
    log_level: str = Field("INFO", alias="LOG_LEVEL")
    db_url: str = Field("sqlite+aiosqlite:///./dev.db", alias="DB_URL")
    test_db_url: str = Field("sqlite+aiosqlite:///./test.db", alias="TEST_DB_URL")
    feature_flags: Dict[str, bool] = Field(default_factory=dict, alias="FEATURE_FLAGS")

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)
