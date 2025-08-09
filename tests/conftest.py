import pytest

from brandnexus.models.document import Document


@pytest.fixture
def sample_doc() -> Document:
    return Document(id="1", content="example")
