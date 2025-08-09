from pydantic import ValidationError
from pydantic_settings import SettingsError as PydanticSettingsError

from .settings import Settings


class EnvironmentError(Exception):
    """Raised when environment variables are invalid."""


def get_settings() -> Settings:
    """Load and validate application settings."""
    try:
        return Settings()
    except (ValidationError, PydanticSettingsError) as exc:
        raise EnvironmentError("Invalid environment configuration") from exc
