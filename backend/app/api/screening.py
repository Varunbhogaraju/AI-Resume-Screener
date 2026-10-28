from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.db import SessionLocal
from backend.app.models.job import Job
from backend.app.models.candidate import Candidate
from backend.app.services.screening_service import ScreeningService
from backend.app.repositories.screening_repository import ScreeningRepository
from backend.app.api.dependencies import get_current_user


router = APIRouter(
    prefix="/api/v1/jobs",
    tags=["Screening"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{job_id}/candidates/{candidate_id}/screen")
def screen_candidate(
    job_id: int,
    candidate_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    candidate = (
        db.query(Candidate)
        .filter(Candidate.id == candidate_id)
        .first()
    )

    if candidate is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found",
        )

    screening_service = ScreeningService(
        ScreeningRepository()
    )

    result = screening_service.screen_candidate(
        db,
        job=job,
        candidate=candidate,
    )

    return result