from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.api.dependencies import get_current_user
from backend.app.db import get_db
from backend.app.models.user import User
from backend.app.repositories.candidate_repository import (
    CandidateRepository,
)
from backend.app.repositories.job_repository import JobRepository
from backend.app.schemas.candidate import CandidateResponse


router = APIRouter(
    prefix="/api/v1/candidates",
    tags=["Candidates"],
)


candidate_repository = CandidateRepository()
job_repository = JobRepository()


@router.get(
    "/{candidate_id}",
    response_model=CandidateResponse,
)
def get_candidate(
    candidate_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    candidate = candidate_repository.get_by_id(
        db,
        candidate_id,
    )

    if candidate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found.",
        )

    job = job_repository.get_by_id(
        db,
        job_id=candidate.job_id,
        owner_id=current_user.id,
    )

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found.",
        )

    return candidate