from sqlalchemy.orm import Session

from backend.app.models.job import Job
from backend.app.repositories.job_repository import JobRepository


class JobService:

    def __init__(
        self,
        job_repository: JobRepository,
    ):
        self.job_repository = job_repository

    def create_job(
        self,
        db: Session,
        *,
        title: str,
        company: str,
        description: str,
        required_skills: str,
        experience_requirement: str,
        location: str,
        employment_type: str,
        owner_id: int,
    ) -> Job:

        return self.job_repository.create(
            db,
            title=title,
            company=company,
            description=description,
            required_skills=required_skills,
            experience_requirement=experience_requirement,
            location=location,
            employment_type=employment_type,
            owner_id=owner_id,
        )

    def get_job(
        self,
        db: Session,
        *,
        job_id: int,
        owner_id: int,
    ) -> Job | None:

        return self.job_repository.get_by_id(
            db,
            job_id=job_id,
            owner_id=owner_id,
        )

    def get_jobs(
        self,
        db: Session,
        *,
        owner_id: int,
    ) -> list[Job]:

        return self.job_repository.get_all_by_owner(
            db,
            owner_id=owner_id,
        )
    def update_job(
        self,
        db: Session,
        *,
        job_id: int,
        owner_id: int,
        updates: dict,
    ) -> Job | None:

        job = self.job_repository.get_by_id(
            db,
            job_id=job_id,
            owner_id=owner_id,
        )

        if job is None:
            return None

        return self.job_repository.update(
            db,
            job=job,
            updates=updates,
        )
    def delete_job(
        self,
        db: Session,
        *,
        job_id: int,
        owner_id: int,
    ) -> bool:

        job = self.job_repository.get_by_id(
            db,
            job_id=job_id,
            owner_id=owner_id,
        )

        if job is None:
            return False

        self.job_repository.delete(
            db,
            job=job,
        )

        return True