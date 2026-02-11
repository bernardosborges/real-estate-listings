from app.domain.entities.user_profile import UserProfile
from app.domain.value_objects.user_profile.user_profile_public_id import UserProfilePublicId


def user_profile_factory(**overrides):
    def _create(**kwargs):
        data = {
            "id": 1,
            "public_id": UserProfilePublicId.from_raw("abc123abc123abc123abc"),
            "user_id": 10,
            "name": None,
            "bio": None,
            "work_phone": None,
            "work_city": None,
            "license_number": None,
            "profile_picture_url": None,
            "background_image_url": None,
            "preferences": {},
            "deleted_at": None,
        }

        data.update(overrides)
        data.update(kwargs)

        return UserProfile(**data)
    return _create