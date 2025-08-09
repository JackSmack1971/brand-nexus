class HelperError(Exception):
    """Helper failure."""


def slugify(name: str) -> str:
    """Slugify a name."""
    raise HelperError("Slugify not implemented")
