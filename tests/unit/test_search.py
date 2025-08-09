import pytest

from brandnexus.core.search import SearchError, search_documents


@pytest.mark.asyncio
async def test_search_error() -> None:
    with pytest.raises(SearchError):
        await search_documents("query")
