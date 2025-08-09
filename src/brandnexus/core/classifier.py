from brandnexus.models.document import Document


class ClassifierError(Exception):
    """Classifier failure."""


async def classify_document(document: Document) -> str:
    """Classify a document."""
    try:
        raise NotImplementedError("Classification not implemented")
    except Exception as exc:  # noqa: BLE001
        raise ClassifierError from exc
