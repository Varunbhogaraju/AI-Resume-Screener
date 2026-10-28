from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from backend.app.api.dependencies import get_current_user
from backend.app.db import get_db
from backend.app.models.user import User
from backend.app.repositories.candidate_repository import (
    CandidateRepository,
)
from backend.app.repositories.job_repository import JobRepository
from backend.app.schemas.candidate import CandidateResponse
from backend.app.services.candidate_service import CandidateService
from backend.app.services.file_storage import (
    generate_storage_filename,
    save_file,
    validate_file,
)
from backend.app.services.resume_parser import extract_resume_text
from backend.app.services.candidate_extractor import (
    extract_candidate_metadata,
)


router = APIRouter(
    prefix="/api/v1/jobs",
    tags=["Candidates"],
)


job_repository = JobRepository()
candidate_repository = CandidateRepository()

candidate_service = CandidateService(
    candidate_repository,
)


@router.post(
    "/{job_id}/candidates",
    response_model=CandidateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_candidate_resume(
    job_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job = job_repository.get_by_id(
        db,
        job_id=job_id,
        owner_id=current_user.id,
    )

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found.",
        )

    file_data = await file.read()

    try:
        validate_file(
            filename=file.filename or "",
            file_size=len(file_data),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    storage_filename = generate_storage_filename(
        file.filename or "resume"
    )

    storage_path = save_file(
        file_data=file_data,
        filename=storage_filename,
    )

    try:
        resume_text = extract_resume_text(
            file_path=Path(storage_path),
            content_type=file.content_type or "",
        )
        metadata = extract_candidate_metadata(
        resume_text,
        )
        name = metadata.get("name")
        email = metadata.get("email")
        phone = metadata.get("phone")

        if not name or not email:
            raise ValueError(
                "Failed to extract candidate name or email from resume."
            )
    except ValueError as exc:
        Path(storage_path).unlink(
            missing_ok=True,
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    candidate = candidate_service.create_candidate(
        db,
        job_id=job.id,
        name=metadata["name"],
        email=metadata["email"],
        phone=metadata["phone"],
        resume_filename=file.filename or "resume",
        resume_path=str(storage_path),
        resume_text=resume_text,
    )

    return candidate

@router.get(
    "/{job_id}/candidates",
    response_model=list[CandidateResponse],
)
def get_candidates_for_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    job = job_repository.get_by_id(
        db,
        job_id=job_id,
        owner_id=current_user.id,
    )

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found.",
        )

    return candidate_service.get_candidates_for_job(
        db,
        job_id=job.id,
    )