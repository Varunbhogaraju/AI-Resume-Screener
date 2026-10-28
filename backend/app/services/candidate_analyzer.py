import re

from backend.app.services.job_analyzer import COMMON_SKILLS


def extract_candidate_skills(
    resume_text: str,
) -> list[str]:

    normalized_text = resume_text.lower()

    found_skills = []

    for skill in COMMON_SKILLS:
        pattern = rf"(?<!\w){re.escape(skill.lower())}(?!\w)"

        if re.search(
            pattern,
            normalized_text,
        ):
            found_skills.append(skill.lower())

    return sorted(set(found_skills))


def extract_candidate_experience(
    resume_text: str,
) -> float | None:

    normalized_text = resume_text.lower()

    pattern = r"(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)"

    matches = re.findall(
        pattern,
        normalized_text,
    )

    if not matches:
        return None

    return max(
        float(match)
        for match in matches
    )


def analyze_candidate(
    resume_text: str,
) -> dict:

    return {
        "skills": extract_candidate_skills(
            resume_text
        ),
        "experience_years": extract_candidate_experience(
            resume_text
        ),
    }