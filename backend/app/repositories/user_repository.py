from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.user import User

class UserRepository:

    def create(
        self,
        db: Session,
        *,
        name: str,
        email: str,
        password_hash: str,
        role: str = "RECRUITER",
    ) ->User:
        user = User(
            name=name,
            email=email,
            password_hash=password_hash,
            role=role,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    def get_by_email(
        self,
        db: Session,
        *,
        email: str,
    ) ->User | None:
        statement = select(User).where(User.email == email)

        return db.scalar(statement)
    def get_by_id(
        self,
        db: Session,
        *,
        user_id: int,
    ) -> User | None:
        statement = select(User).where(User.id == user_id)

        return db.scalar(statement)