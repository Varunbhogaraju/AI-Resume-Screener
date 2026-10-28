from pathlib import Path
from uuid import uuid4


UPLOAD_DIRECTORY = Path("uploads")

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
}

MAX_FILE_SIZE = 5 * 1024 * 1024 


def validate_file(
    filename: str,
    file_size: int,
) -> str:

    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Unsupported file type. Only PDF and DOCX files are allowed."
        )

    if file_size > MAX_FILE_SIZE:
        raise ValueError(
            "File is too large. Maximum allowed size is 5 MB."
        )

    return extension


def generate_storage_filename(
    original_filename: str,
) -> str:

    extension = Path(original_filename).suffix.lower()

    return f"{uuid4().hex}{extension}"


def save_file(
    file_data: bytes,
    filename: str,
) -> Path:

    UPLOAD_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    storage_path = UPLOAD_DIRECTORY / filename

    storage_path.write_bytes(file_data)

    return storage_path