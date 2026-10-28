from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db import Base

class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    company: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    required_skills: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
    )

    experience_requirement: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="",
    )

    location: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        default="",
    )

    employment_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="Full-time",
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )