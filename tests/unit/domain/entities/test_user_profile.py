import pytest

from app.domain.entities.user_profile import UserProfile
from app.domain.exceptions.domain_exception import FieldTooLong
from app.domain.value_objects.user_profile.user_profile_public_id import UserProfilePublicId
from app.domain.exceptions.domain_exception import AlreadyDeleted, CannotBeRestored
from app.domain.constants.user_profile_constants import (
    PROFILE_NAME_MAX_LENGHT,
    PROFILE_BIO_MAX_LENGHT,
    PROFILE_WORK_PHONE_MAX_LENGHT,
    PROFILE_WORK_CITY_MAX_LENGHT,
    PROFILE_LICENSE_NUMBER_MAX_LENGHT
)


# -------------------- TEST USER_PROFILE CREATION --------------------

def test_create_user_profile_defaults(user_profile_factory):
    user_profile = user_profile_factory()
    assert user_profile.name is None
    assert user_profile.bio is None
    assert user_profile.preferences == {}
    assert user_profile.is_deleted is False


# -------------------- TEST IS_DELETED  --------------------

def test_is_deleted_reflects_deleted_at(user_profile_factory):
    user_profile = user_profile_factory()
    assert user_profile.is_deleted is False
    user_profile.soft_delete()
    assert user_profile.is_deleted is True


# -------------------- TEST SOFT_DELETE --------------------

def test_soft_delete_sets_deleted_at(user_profile_factory):
    user_profile = user_profile_factory()
    user_profile.soft_delete()
    assert user_profile.deleted_at is not None
    assert user_profile.is_deleted is True


def test_soft_deleted_twice_raises_exception(user_profile_factory):
    user_profile = user_profile_factory()
    user_profile.soft_delete()
    with pytest.raises(AlreadyDeleted):
        user_profile.soft_delete()


# -------------------- TEST RESTORE --------------------

def test_restore_clears_deleted_at(user_profile_factory):
    user_profile = user_profile_factory()
    user_profile.soft_delete()
    user_profile.restore()
    assert user_profile.deleted_at is None
    assert user_profile.is_deleted is False

def test_restore_without_delete_raises_exception(user_profile_factory):
    user_profile = user_profile_factory()
    with pytest.raises(CannotBeRestored):
        user_profile.restore()


# -------------------- TEST UPDATE_BASIC_INFO --------------------

def test_update_basic_info_updates_fields(user_profile_factory):
    user_profile = user_profile_factory()
    user_profile.update_basic_info(
        name="John Doe",
        bio="Real estate agent",
        work_city="Porto Alegre"
    )
    assert user_profile.name == "John Doe"
    assert user_profile.bio == "Real estate agent"
    assert user_profile.work_city == "Porto Alegre"


def test_update_basic_info_partial_update(user_profile_factory):
    user_profile = user_profile_factory(name="Old name")
    user_profile.update_basic_info(name="New name")
    assert user_profile.name == "New name"
    assert user_profile.bio is None


# -------------------- TEST FIELDS --------------------

@pytest.mark.parametrize(
    "field_name,max_length",
    [
        ("name", PROFILE_NAME_MAX_LENGHT),
        ("bio", PROFILE_BIO_MAX_LENGHT),
        ("work_phone", PROFILE_WORK_PHONE_MAX_LENGHT),
        ("work_city", PROFILE_WORK_CITY_MAX_LENGHT),
        ("license_number", PROFILE_LICENSE_NUMBER_MAX_LENGHT)
    ]
)
def test_fields_too_long(user_profile_factory, field_name, max_length):
    user_profile = user_profile_factory()
    invalid_value = "A" * (max_length + 1)
    with pytest.raises(FieldTooLong):
        user_profile.update_basic_info(**{field_name: invalid_value})


