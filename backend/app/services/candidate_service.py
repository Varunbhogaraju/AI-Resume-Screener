from sqlalchemy.orm import Session

from backend.app.repositories.candidate_repository import (
    CandidateRepository,
)


class CandidateService:

    def __init__(
        self,
        candidate_repository: CandidateRepository,
    ):
        self.candidate_repository = candidate_repository

    def create_candidate(
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
    ):

        return self.candidate_repository.create(
            db,
            job_id=job_id,
            name=name,
            email=email,
            phone=phone,
            resume_filename=resume_filename,
            resume_path=resume_path,
            resume_text=resume_text,
        )

    def get_candidate(
        self,
        db: Session,
        candidate_id: int,
    ):

        return self.candidate_repository.get_by_id(
            db,
            candidate_id,
        )

    def get_candidates_for_job(
        self,
        db: Session,
        job_id: int,
    ):

        return self.candidate_repository.get_by_job_id(
            db,
            job_id,
        )