from __future__ import annotations

import pytest

from brandnexus.config.environment import EnvironmentError, get_settings


def test_get_settings_defaults(monkeypatch):
    monkeypatch.delenv("APP_ENV", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    monkeypatch.delenv("DB_URL", raising=False)
    monkeypatch.delenv("TEST_DB_URL", raising=False)
    monkeypatch.delenv("FEATURE_FLAGS", raising=False)

    settings = get_settings()

    assert settings.app_env == "development"
    assert settings.log_level == "INFO"
    assert settings.db_url.startswith("sqlite")
    assert settings.test_db_url.startswith("sqlite")
    assert settings.feature_flags == {}


def test_get_settings_env_override(monkeypatch):
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("DB_URL", "sqlite+aiosqlite:///./custom.db")
    monkeypatch.setenv("TEST_DB_URL", "sqlite+aiosqlite:///./custom-test.db")
    monkeypatch.setenv("FEATURE_FLAGS", '{"new": true}')

    settings = get_settings()

    assert settings.app_env == "test"
    assert settings.log_level == "DEBUG"
    assert settings.db_url.endswith("custom.db")
    assert settings.test_db_url.endswith("custom-test.db")
    assert settings.feature_flags["new"] is True


def test_invalid_feature_flags(monkeypatch):
    monkeypatch.setenv("FEATURE_FLAGS", "invalid-json")

    with pytest.raises(EnvironmentError):
        get_settings()
