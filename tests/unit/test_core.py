import pytest

from brandnexus.config.environment import get_settings
from brandnexus.core.classifier import ClassifierError, classify_document
from brandnexus.core.database import DatabaseError, connect_db
from brandnexus.core.indexer import IndexerError, index_document
from brandnexus.core.search import SearchError, search_documents
from brandnexus.main import main
from brandnexus.models.document import Document
from brandnexus.utils.file_utils import FileError, read_file
from brandnexus.utils.helpers import HelperError, slugify


@pytest.mark.asyncio
async def test_stubs() -> None:
    doc = Document(id="1", content="x")
    with pytest.raises(IndexerError):
        await index_document(doc)
    with pytest.raises(ClassifierError):
        await classify_document(doc)
    with pytest.raises(SearchError):
        await search_documents("x")
    with pytest.raises(DatabaseError):
        await connect_db("url")
    with pytest.raises(FileError):
        await read_file("path")
    with pytest.raises(HelperError):
        slugify("name")
    settings = get_settings()
    assert settings.api_key == ""
    await main()
