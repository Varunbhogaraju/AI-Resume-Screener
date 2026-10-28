def calculate_skill_match(
    required_skills: list[str],
    candidate_skills: list[str],
) -> dict:

    required = set(
        skill.lower()
        for skill in required_skills
    )

    candidate = set(
        skill.lower()
        for skill in candidate_skills
    )

    if not required:
        return {
            "score": 0.0,
            "matched_skills": [],
            "missing_skills": [],
        }

    matched = sorted(
        required.intersection(candidate)
    )

    missing = sorted(
        required.difference(candidate)
    )

    score = (
        len(matched) / len(required)
    ) * 100

    return {
        "score": round(score, 2),
        "matched_skills": matched,
        "missing_skills": missing,
    }


def calculate_experience_match(
    required_years: float | None,
    candidate_years: float | None,
) -> float:

    if required_years is None:
        return 100.0

    if candidate_years is None:
        return 0.0

    if candidate_years >= required_years:
        return 100.0

    return round(
        (candidate_years / required_years) * 100,
        2,
    )


def calculate_overall_score(
    skill_score: float,
    experience_score: float,
) -> float:

    score = (
        skill_score * 0.75
        + experience_score * 0.25
    )

    return round(
        score,
        2,
    )
def get_recommendation(score: float) -> str:
    if score >= 80:
        return "Strong Match"
    elif score >= 60:
        return "Potential Match"
    else:
        return "Weak Match"