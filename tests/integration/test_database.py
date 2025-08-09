import pytest

from brandnexus.core.database import DatabaseError, connect_db


@pytest.mark.asyncio
async def test_database_integration_error() -> None:
    with pytest.raises(DatabaseError):
        await connect_db("sqlite:///:memory:")
