from brandnexus.models.document import Document


class IndexerError(Exception):
    """Indexer failure."""


async def index_document(document: Document) -> None:
    """Index a document."""
    try:
        raise NotImplementedError("Indexing not implemented")
    except Exception as exc:  # noqa: BLE001
        raise IndexerError from exc
