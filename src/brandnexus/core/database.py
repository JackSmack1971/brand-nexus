class DatabaseError(Exception):
    """Database failure."""


async def connect_db(url: str) -> None:
    """Connect to a database."""
    try:
        raise NotImplementedError("Database connection not implemented")
    except Exception as exc:  # noqa: BLE001
        raise DatabaseError from exc
