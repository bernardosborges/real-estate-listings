from app.domain.entities.user import User


def user_factory(**overrides):
    def _create(**kwargs):
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
        data.update(kwargs)

        return User(**data)
    return _create