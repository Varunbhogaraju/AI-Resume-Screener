from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.candidate import Candidate


class CandidateRepository:

    def create(
        self,
        db: Session,
        *,
        job_id: int,
        name: str,
        email: str,
        phone: str | None,
        resume_filename: str,
        resume_path: str,
        resume_text: str,
    ) -> Candidate:

        candidate = Candidate(
            job_id=job_id,
            name=name,
            email=email,
            phone=phone,
            resume_filename=resume_filename,
            resume_path=resume_path,
            resume_text=resume_text,
        )

        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        return candidate

    def get_by_id(
        self,
        db: Session,
        candidate_id: int,
    ) -> Candidate | None:

        statement = select(Candidate).where(
            Candidate.id == candidate_id
        )

        return db.execute(statement).scalar_one_or_none()

    def get_by_job_id(
        self,
        db: Session,
        job_id: int,
    ) -> list[Candidate]:

        statement = (
            select(Candidate)
            .where(Candidate.job_id == job_id)
            .order_by(Candidate.created_at.desc())
        )

        return list(
            db.execute(statement).scalars().all()
        )