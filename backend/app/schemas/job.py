from datetime import datetime

from pydantic import BaseModel, Field

class JobCreateRequest(BaseModel):
    title: str = Field(
        min_length=2,
        max_length=200,
    )

    company: str = Field(
        min_length=2,
        max_length=200,
    )

    description: str = Field(
        min_length=20,
    )

    required_skills: str = ""

    experience_requirement: str = ""

    location: str = ""

    employment_type: str = "Full-time"
    
class JobUpdateRequest(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=200,
    )

    company: str | None = Field(
        default=None,
        min_length=2,
        max_length=200,
    )

    description: str | None = Field(
        default=None,
        min_length=20,
    )

    required_skills: str | None = None

    experience_requirement: str | None = None

    location: str | None = None

    employment_type: str | None = None

class JobResponse(BaseModel):
    id: int
    title: str
    company: str
    description: str
    required_skills: str
    experience_requirement: str
    location: str
    employment_type: str
    owner_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }