import pytest
from unittest.mock import Mock

from app.domain.entities.user import User


@pytest.fixture
def user():
    return User(
        id=1,
        email="user@test.com",
        password_hash="hashed-password",
        is_active=True
    )

def test_create_user_with_required_fields():
    user = User(
        id=1,
        email="user@test.com",
        password_hash="hashed-password",
        is_active=True
    )

    assert user.id == 1
    assert user.email == "user@test.com"
    assert user.password_hash == "hashed-password"
    assert user.is_active is True
    assert user.is_verified is False
    assert user.is_superuser is False
    assert user.profile is None


def test_activate_user(user):
    user.activate()
    assert user.is_active is True


def test_deactivate_user(user):
    user.deactivate()
    assert user.is_active is False

def test_attach_profile_to_user(user):
    profile = Mock()
    user.attach_profile(profile)
    assert user.profile is profile