from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.job import Job


class JobRepository:

    def create(
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

        job = Job(
            title=title,
            company=company,
            description=description,
            required_skills=required_skills,
            experience_requirement=experience_requirement,
            location=location,
            employment_type=employment_type,
            owner_id=owner_id,
        )

        db.add(job)
        db.commit()
        db.refresh(job)

        return job

    def get_by_id(
        self,
        db: Session,
        *,
        job_id: int,
        owner_id: int,
    ) -> Job | None:

        statement = select(Job).where(
            Job.id == job_id,
            Job.owner_id == owner_id,
        )

        return db.scalar(statement)

    def get_all_by_owner(
        self,
        db: Session,
        *,
        owner_id: int,
    ) -> list[Job]:

        statement = (
            select(Job)
            .where(Job.owner_id == owner_id)
            .order_by(Job.created_at.desc())
        )

        return list(db.scalars(statement).all())
    
    def update(
        self,
        db: Session,
        *,
        job: Job,
        updates: dict,
    ) -> Job:

        for field, value in updates.items():
            setattr(job, field, value)

        db.commit()
        db.refresh(job)

        return job

    def delete(
        self,
        db: Session,
        *,
        job: Job,
    ) -> None:

        db.delete(job)
        db.commit()