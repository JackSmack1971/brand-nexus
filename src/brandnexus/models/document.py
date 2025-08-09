from pydantic import BaseModel


class Document(BaseModel):
    """Text document."""

    id: str
    content: str
