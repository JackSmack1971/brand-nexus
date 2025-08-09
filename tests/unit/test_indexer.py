import pytest

from brandnexus.models.document import Document
from brandnexus.core.indexer import IndexerError, index_document
from brandnexus.utils.file_utils import FileError, read_file
from brandnexus.utils.helpers import HelperError, slugify


@pytest.mark.asyncio
async def test_indexer_and_utils(sample_doc: Document) -> None:
    with pytest.raises(IndexerError):
        await index_document(sample_doc)
    with pytest.raises(FileError):
        await read_file("missing.txt")
    with pytest.raises(HelperError):
        slugify("Example Name")
