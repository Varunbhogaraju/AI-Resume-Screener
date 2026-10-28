from datetime import datetime

from pydantic import BaseModel, EmailStr


class CandidateCreateRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None


class CandidateResponse(BaseModel):
    id: int
    job_id: int
    name: str
    email: EmailStr
    phone: str | None
    resume_filename: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }