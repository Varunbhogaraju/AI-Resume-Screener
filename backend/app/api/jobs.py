from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.api.dependencies import get_current_user
from backend.app.db import get_db
from backend.app.models.user import User
from backend.app.repositories.job_repository import JobRepository
from backend.app.schemas.job import JobCreateRequest, JobResponse, JobUpdateRequest
from backend.app.services.job_service import JobService


router = APIRouter(
    prefix="/api/v1/jobs",
    tags=["Jobs"],
)


job_repository = JobRepository()
job_service = JobService(job_repository)


@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_job(
    payload: JobCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return job_service.create_job(
        db,
        title=payload.title,
        company=payload.company,
        description=payload.description,
        required_skills=payload.required_skills,
        experience_requirement=payload.experience_requirement,
        location=payload.location,
        employment_type=payload.employment_type,
        owner_id=current_user.id,
    )


@router.get(
    "",
    response_model=list[JobResponse],
)
def get_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return job_service.get_jobs(
        db,
        owner_id=current_user.id,
    )


@router.get(
    "/{job_id}",
    response_model=JobResponse,
)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job = job_service.get_job(
        db,
        job_id=job_id,
        owner_id=current_user.id,
    )

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found.",
        )

    return job

@router.patch(
    "/{job_id}",
    response_model=JobResponse,
)
def update_job(
    job_id: int,
    payload: JobUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updates = payload.model_dump(
        exclude_unset=True,
    )

    if not updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update.",
        )

    job = job_service.update_job(
        db,
        job_id=job_id,
        owner_id=current_user.id,
        updates=updates,
    )

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found.",
        )

    return job

@router.delete(
    "/{job_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = job_service.delete_job(
        db,
        job_id=job_id,
        owner_id=current_user.id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found.",
        )