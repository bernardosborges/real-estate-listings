import pytest

from app.domain.entities.user import User


@pytest.fixture
def user_factory():
    def _create(**overrides):
        data = {
            "id": 1,
            "email": "user@test.com",
            "password_hash": "hashed-password",
            "is_active": True,
            "is_verified": False,
            "is_superuser": False,
            "profile": None,
        }

        data.update(overrides)

        return User(**data)
    return _create