from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db import Base


class ScreeningResult(Base):
    __tablename__ = "screening_results"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    candidate_id: Mapped[int] = mapped_column(
        ForeignKey("candidates.id"),
        nullable=False,
        index=True,
    )

    job_id: Mapped[int] = mapped_column(
        ForeignKey("jobs.id"),
        nullable=False,
        index=True,
    )

    overall_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    skill_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    experience_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    matched_skills: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
    )

    missing_skills: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
    )

    recommendation: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )