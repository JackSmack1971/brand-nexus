import pytest

from brandnexus.core.database import DatabaseError, connect_db
from brandnexus.config.environment import get_settings
from brandnexus.main import main


@pytest.mark.asyncio
async def test_database_and_config() -> None:
    with pytest.raises(DatabaseError):
        await connect_db("sqlite:///:memory:")
    settings = get_settings()
    assert settings.db_url.startswith("sqlite")
    await main()
