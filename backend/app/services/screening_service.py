from sqlalchemy.orm import Session

from backend.app.models.candidate import Candidate
from backend.app.models.job import Job

from backend.app.repositories.screening_repository import (
    ScreeningRepository,
)

from backend.app.services.candidate_analyzer import (
    analyze_candidate,
)

from backend.app.services.job_analyzer import (
    analyze_job,
)

from backend.app.services.resume_ai_analyzer import (
    analyze_resume_with_ai,
)

from backend.app.services.ai_matching import (
    analyze_semantic_match,
)

from backend.app.services.matching_engine import (
    calculate_experience_match,
    calculate_overall_score,
    calculate_skill_match,
    get_recommendation,
)


class ScreeningService:

    def __init__(
        self,
        screening_repository: ScreeningRepository,
    ):
        self.screening_repository = screening_repository

    def screen_candidate(
        self,
        db: Session,
        *,
        job: Job,
        candidate: Candidate,
    ):
        job_analysis = analyze_job(
            description=job.description,
            required_skills=job.required_skills,
            experience_requirement=job.experience_requirement,
        )

        candidate_analysis = analyze_candidate(
            candidate.resume_text,
        )

        try:
            ai_candidate_analysis = analyze_resume_with_ai(
                candidate.resume_text,
            )
        except Exception as exc:
            print(
                f"AI resume analysis failed. "
                f"Using deterministic analysis only: {exc}"
            )
            ai_candidate_analysis = None

        try:
            ai_match_analysis = analyze_semantic_match(
                job_description=job.description,
                required_skills=job.required_skills,
                resume_text=candidate.resume_text,
            )
        except Exception as exc:
            print(
                f"AI semantic matching failed. "
                f"Using deterministic matching only: {exc}"
            )
            ai_match_analysis = None

        skill_result = calculate_skill_match(
            required_skills=job_analysis[
                "required_skills"
            ],
            candidate_skills=candidate_analysis[
                "skills"
            ],
        )

        if ai_match_analysis is not None:
            ai_matched_skills = [
                item.skill
                for item in ai_match_analysis.skill_evidence
                if item.matched
            ]

            ai_missing_skills = [
                item.skill
                for item in ai_match_analysis.skill_evidence
                if not item.matched
            ]

            matched_skills = ai_matched_skills
            missing_skills = ai_missing_skills

        else:
            matched_skills = skill_result[
                "matched_skills"
            ]

            missing_skills = skill_result[
                "missing_skills"
            ]

        required_experience = (
            self._extract_required_experience(
                job.experience_requirement
            )
        )

        experience_score = calculate_experience_match(
            required_years=required_experience,
            candidate_years=candidate_analysis[
                "experience_years"
            ],
        )

        overall_score = calculate_overall_score(
            skill_score=skill_result["score"],
            experience_score=experience_score,
        )

        recommendation = get_recommendation(
            overall_score,
        )

        result = self.screening_repository.create(
            db,
            candidate_id=candidate.id,
            job_id=job.id,
            overall_score=overall_score,
            skill_score=skill_result["score"],
            experience_score=experience_score,
            matched_skills=",".join(
                matched_skills
            ),
            missing_skills=",".join(
                missing_skills
            ),
            recommendation=recommendation,
        )

        return result

    @staticmethod
    def _extract_required_experience(
        experience_requirement: str,
    ) -> float | None:

        import re

        if not experience_requirement:
            return None

        match = re.search(
            r"(\d+(?:\.\d+)?)",
            experience_requirement,
        )

        if not match:
            return None

        return float(match.group(1))