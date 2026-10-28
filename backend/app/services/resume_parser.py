from pathlib import Path

from docx import Document
from pypdf import PdfReader


PDF_CONTENT_TYPE = "application/pdf"

DOCX_CONTENT_TYPE = (
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)


def extract_text_from_pdf(file_path: Path) -> str:
    reader = PdfReader(str(file_path))

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages).strip()


def extract_text_from_docx(file_path: Path) -> str:
    document = Document(str(file_path))

    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return "\n".join(paragraphs).strip()


def extract_resume_text(
    file_path: Path,
    content_type: str,
) -> str:

    if content_type == PDF_CONTENT_TYPE:

        text = extract_text_from_pdf(file_path)

    elif content_type == DOCX_CONTENT_TYPE:

        text = extract_text_from_docx(file_path)

    else:

        raise ValueError(
            "Unsupported resume file type."
        )

    if not text:

        raise ValueError(
            "Could not extract text from the uploaded resume."
        )

    return text