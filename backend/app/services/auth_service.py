from sqlalchemy.orm import Session

from backend.app.models.user import User
from backend.app.repositories.user_repository import UserRepository
from backend.app.utils.security import hash_password, verify_password


class AuthService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(
        self,
        db: Session,
        *,
        name: str,
        email: str,
        password: str,
    ) -> User:

        existing_user = self.user_repository.get_by_email(
            db,
            email=email,
        )

        if existing_user is not None:
            raise ValueError("A user with this email already exists.")

        password_hash = hash_password(password)

        return self.user_repository.create(
            db,
            name=name,
            email=email,
            password_hash=password_hash,
        )

    def authenticate_user(
        self,
        db: Session,
        *,
        email: str,
        password: str,
    ) -> User | None:
        user = self.user_repository.get_by_email(
            db,
            email=email,
        )

        if user is None:
            return None

        if not verify_password(
            password,
            user.password_hash,
        ):
            return None

        return user