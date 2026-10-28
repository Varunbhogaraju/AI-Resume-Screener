from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.screening_result import ScreeningResult


class ScreeningRepository:

    def create(
        self,
        db: Session,
        *,
        candidate_id: int,
        job_id: int,
        overall_score: float,
        skill_score: float,
        experience_score: float,
        matched_skills: str,
        missing_skills: str,
        recommendation: str,
    ) -> ScreeningResult:

        result = ScreeningResult(
            candidate_id=candidate_id,
            job_id=job_id,
            overall_score=overall_score,
            skill_score=skill_score,
            experience_score=experience_score,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            recommendation=recommendation,
        )

        db.add(result)
        db.commit()
        db.refresh(result)

        return result

    def get_latest_for_candidate(
        self,
        db: Session,
        *,
        candidate_id: int,
        job_id: int,
    ) -> ScreeningResult | None:

        statement = (
            select(ScreeningResult)
            .where(
                ScreeningResult.candidate_id == candidate_id,
                ScreeningResult.job_id == job_id,
            )
            .order_by(
                ScreeningResult.created_at.desc()
            )
        )

        return db.scalar(statement)