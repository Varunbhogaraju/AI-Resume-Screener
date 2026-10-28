import re


COMMON_SKILLS = {
    "python",
    "java",
    "javascript",
    "typescript",
    "c",
    "c++",
    "c#",
    "go",
    "rust",
    "sql",
    "postgresql",
    "mysql",
    "mongodb",
    "redis",
    "fastapi",
    "django",
    "flask",
    "spring",
    "node.js",
    "react",
    "angular",
    "vue",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "git",
    "linux",
    "rest",
    "graphql",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "pandas",
    "numpy",
}


def normalize_text(text: str) -> str:
    return re.sub(
        r"\s+",
        " ",
        text.lower(),
    ).strip()


def extract_required_skills(
    required_skills: str,
) -> list[str]:

    skills = []

    for skill in required_skills.split(","):
        normalized = normalize_text(skill)

        if normalized and normalized not in skills:
            skills.append(normalized)

    return skills


def extract_skills_from_text(
    text: str,
) -> list[str]:

    normalized_text = normalize_text(text)

    found_skills = []

    for skill in COMMON_SKILLS:
        pattern = rf"(?<!\w){re.escape(skill)}(?!\w)"

    if re.search(
        pattern,
        normalized_text,
    ):
        found_skills.append(skill)

    return sorted(found_skills)


def extract_experience_years(
    text: str,
) -> float | None:

    normalized_text = normalize_text(text)

    patterns = [
        r"(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)",
    ]

    for pattern in patterns:
        matches = re.findall(
            pattern,
            normalized_text,
        )

        if matches:
            return max(
                float(match)
                for match in matches
            )

    return None


def analyze_job(
    description: str,
    required_skills: str,
    experience_requirement: str,
) -> dict:

    skills = extract_required_skills(
        required_skills
    )

    description_skills = extract_skills_from_text(
        description
    )

    combined_skills = list(
        dict.fromkeys(
            skills + description_skills
        )
    )

    return {
        "required_skills": combined_skills,
        "experience_requirement": experience_requirement,
    }