from unittest.mock import Mock
import pytest


@pytest.mark.unit
def test_create_user_with_required_fields(user_factory_fixture):
    user = user_factory_fixture()

    assert user.id == 1
    assert user.email == "user@test.com"
    assert user.password_hash == "hashed-password"
    assert user.is_active is True
    assert user.is_verified is False
    assert user.is_superuser is False
    assert user.profile is None


@pytest.mark.unit
def test_activate_user(user_factory_fixture):
    user = user_factory_fixture(is_active=False)
    user.activate()
    assert user.is_active is True


@pytest.mark.unit
def test_deactivate_user(user_factory_fixture):
    user = user_factory_fixture(is_active=True)
    user.deactivate()
    assert user.is_active is False


@pytest.mark.unit
def test_attach_profile_to_user(user_factory_fixture):
    user = user_factory_fixture()
    profile = Mock()
    user.attach_profile(profile)
    assert user.profile is profile
