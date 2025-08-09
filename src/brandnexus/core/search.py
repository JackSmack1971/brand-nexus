class SearchError(Exception):
    """Search failure."""


async def search_documents(query: str) -> list[str]:
    """Search for documents."""
    try:
        raise NotImplementedError("Search not implemented")
    except Exception as exc:  # noqa: BLE001
        raise SearchError from exc
