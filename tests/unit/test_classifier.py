import pytest

from brandnexus.models.document import Document
from brandnexus.core.classifier import ClassifierError, classify_document


@pytest.mark.asyncio
async def test_classifier_error(sample_doc: Document) -> None:
    with pytest.raises(ClassifierError):
        await classify_document(sample_doc)
