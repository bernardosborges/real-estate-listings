from __future__ import annotations
from app.domain.entities.user import User
from app.domain.value_objects.user.user_email import UserEmail


class UserFactory:

    @staticmethod
    def create(*, email: UserEmail, password_hash: str, is_superuser: bool = False) -> User:

        return User(
            id=None,
            email=email,
            password_hash=password_hash,
            is_active=True,
            is_verified=False,
            is_superuser=is_superuser,
        )
