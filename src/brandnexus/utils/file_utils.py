class FileError(Exception):
    """File utility failure."""


async def read_file(path: str) -> str:
    """Read a file."""
    try:
        raise NotImplementedError("File read not implemented")
    except Exception as exc:  # noqa: BLE001
        raise FileError from exc
