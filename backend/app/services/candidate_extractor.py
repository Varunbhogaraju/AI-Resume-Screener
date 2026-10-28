import re


EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)


PHONE_PATTERN = re.compile(
    r"(?<!\d)"
    r"(?:\+91[\s-]?)?"
    r"(?:\d[\s-]?){10}"
    r"(?!\d)"
)


def extract_email(text: str) -> str | None:
    match = EMAIL_PATTERN.search(text)

    if match:
        return match.group(0)

    return None


def extract_phone(text: str) -> str | None:
    match = PHONE_PATTERN.search(text)

    if not match:
        return None

    phone = re.sub(
        r"[^\d+]",
        "",
        match.group(0),
    )

    return phone


def extract_name(text: str) -> str | None:
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    ignored_prefixes = (
        "email",
        "phone",
        "mobile",
        "contact",
        "address",
        "linkedin",
        "github",
        "resume",
        "curriculum vitae",
        "cv",
    )

    for line in lines[:10]:
        normalized = line.lower()

        if normalized.startswith(ignored_prefixes):
            continue

        if "@" in line:
            continue

        if any(char.isdigit() for char in line):
            continue

        words = line.split()

        if 2 <= len(words) <= 5:
            return line

    return None


def extract_candidate_metadata(
    text: str,
) -> dict[str, str | None]:

    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
    }