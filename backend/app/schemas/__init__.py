from backend.app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from backend.app.schemas.job import (
    JobCreateRequest,
    JobResponse,
    JobUpdateRequest,
)
from backend.app.schemas.candidate import (
    CandidateCreateRequest,
    CandidateResponse,
)
__all__ = [
    "LoginRequest",
    "RegisterRequest",
    "TokenResponse",
    "UserResponse",
    "JobCreateRequest",
    "JobResponse",
    "JobUpdateRequest",
    "CandidateCreateRequest",
    "CandidateResponse",
]
